import edu.stanford.nlp.ie.machinereading.structure.MachineReadingAnnotations;
import edu.stanford.nlp.ie.machinereading.structure.RelationMention;
import edu.stanford.nlp.ie.util.RelationTriple;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.naturalli.NaturalLogicAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLPClient;
import edu.stanford.nlp.simple.Document;
import edu.stanford.nlp.simple.Sentence;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.PropertiesUtils;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by dell on 14/03/2017.
 */
public class CoreDemo {
    public static void main(String[] args) throws IOException {
        DatabaseConnection databaseConnection = new DatabaseConnection();
        int numDocuments = 0, numSentences = 0;

        System.out.println("test");

        long start = System.currentTimeMillis();

        // read some text in the text variable
        String text = "Obama lives in Washington and George lives in New York.";
        text = "The City of New York, often called New York City or simply New York, is the most populous city in the United States. " +
                "With an estimated 2016 population of 8,537,673 distributed over a land area of about 302,6 square miles (784 km2), " +
                "New York City is also the most densely populated major city in the United States.";
        FetchURLData fetchURLData = new FetchURLData();

        //267 links
        Set<String> linkSet = fetchURLData.getLinks("https://en.wikipedia.org/wiki/List_of_the_100_largest_population_centres_in_Canada",
                new String[]{"https://tools.wmflabs.org/geohack/geohack", "List_of_the_100_largest_population_centres_in_Canada", "index.php?"});

        //text = fetchURLData.getData("https://en.wikipedia.org/wiki/New_York_City");
        //text = fetchURLData.getData("https://en.wikipedia.org/wiki/Jersey_City,_New_Jersey");


        for (Object link : linkSet) {
            System.out.println("Document: "+ numDocuments++);
            text = fetchURLData.getData(link.toString());

            //run annotation relation extractor (openie)
            String[] textSentences = text.split("\\. ");

            for (String textSentence : textSentences) {
                System.out.println("Sentence: "+ numSentences++);
                annotation_extractor(textSentence.split("\\, "), databaseConnection);
            }


        }

        long end = System.currentTimeMillis();

        System.out.println("Time: " + (end - start));

    }


    public static void process_sentences_core(String text){
        int contSent = 0, contRel = 0;
        DatabaseConnection databaseConnection = new DatabaseConnection();
        Properties props = new Properties();

        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, relation");
        StanfordCoreNLPClient pipeline = new StanfordCoreNLPClient(props, "localhost", 9000, 6);

        // Annotate an example document.
        String[] sentencesText = text.split("\\.");

        for (String sentenceText : sentencesText){

            Annotation document = new Annotation(sentenceText);

            // run all Annotators on this text
            pipeline.annotate(document);

            // these are all the sentences in this document
            // a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
            List<CoreMap> sentences = document.get(CoreAnnotations.SentencesAnnotation.class);

            for(CoreMap sentence: sentences) {
                // traversing the words in the current sentence
                // a CoreLabel is a CoreMap with additional token-specific methods
                for (CoreLabel token: sentence.get(CoreAnnotations.TokensAnnotation.class)) {
                    // this is the text of the token
                    String word = token.get(CoreAnnotations.TextAnnotation.class);
                    // this is the POS tag of the token
                    //String pos = token.get(CoreAnnotations.PartOfSpeechAnnotation.class);
                    // this is the NER label of the token
                    String ne = token.get(CoreAnnotations.NamedEntityTagAnnotation.class);

                    //System.out.println("POS: "+pos);
                    //System.out.print("WORD: "+word);
                    //System.out.println(" | NE: "+ne);
                }

                relation_mention_extractor(sentence, databaseConnection, contRel);

                // this is the parse tree of the current sentence
                //Tree tree = sentence.get(TreeCoreAnnotations.TreeAnnotation.class);

                // this is the Stanford dependency graph of the current sentence
                //SemanticGraph dependencies = sentence.get(SemanticGraphCoreAnnotations.CollapsedCCProcessedDependenciesAnnotation.class);
            }
        }
    }

    public static void relation_mention_extractor(CoreMap sentence, DatabaseConnection databaseConnection, int contRel){
        ArrayList<String> datas = new ArrayList<String>();
        List<RelationMention> relationMentions = sentence.get(MachineReadingAnnotations.RelationMentionsAnnotation.class);

        for (RelationMention relationMention : relationMentions){
            datas = new ArrayList<String>();
            datas.add(relationMention.getEntityMentionArgs().get(0).getType());
            datas.add(relationMention.getEntityMentionArgs().get(0).getValue());
            datas.add(relationMention.getType());
            datas.add(relationMention.getEntityMentionArgs().get(1).getType());
            datas.add(relationMention.getEntityMentionArgs().get(1).getValue());

            datas.add(String.valueOf(Collections.max(relationMention.getTypeProbabilities().values())));

            //Warning: Attempt to make only one statement for all relations
            databaseConnection.prepareStatement(datas);
            System.out.printf("Storing Relation extraction %d\n", +contRel++);
        }
    }

    public static void annotation_extractor(String[] textSentences, DatabaseConnection databaseConnection){
        ArrayList<String> datas = new ArrayList<String>();

        StanfordCoreNLPClient pipeline = new StanfordCoreNLPClient(PropertiesUtils.asProperties(
                "annotators", "tokenize,ssplit,pos,lemma,ner,depparse,natlog,openie",
                "ner.model", "edu/stanford/nlp/models/ner/english.all.3class.distsim.crf.ser.gz",
                "ner.useSUTime", "false",
                "ner.applyNumericClassifiers", "false"), "localhost", 9000, 6);

        // Annotate an example document.

        for (String text : textSentences){
            Annotation doc = new Annotation(text);
            pipeline.annotate(doc);

            // Loop over sentences in the document
            for (CoreMap sentence : doc.get(CoreAnnotations.SentencesAnnotation.class)) {

                // Get the OpenIE triples for the sentence
                Collection<RelationTriple> triples = sentence.get(NaturalLogicAnnotations.RelationTriplesAnnotation.class);

                // Print the triples
                List<RelationTriple> withNE = triples.stream()
                        // make sure the subject is entirely named entities
                        .filter(triple ->
                                triple.subject.stream().noneMatch(token -> "O".equals(token.ner())))
                        // make sure the object is entirely named entities
                        .filter(triple ->
                                triple.object.stream().noneMatch(token -> "O".equals(token.ner())))
                        // Convert the stream back to a list
                        .collect(Collectors.toList());

                if (!withNE.isEmpty()) {
                    RelationTriple selectedTriple = Collections.max(withNE);

                    int count = 0;
                    datas.clear();

                    if(!selectedTriple.subject.isEmpty() && !selectedTriple.relation.isEmpty() && !selectedTriple.object.isEmpty()) {
                        System.out.printf("Triple %d\n", count+1);
                        datas.add(selectedTriple.subject.get(0).ner());
                        datas.add(selectedTriple.subjectLemmaGloss());
                        datas.add(selectedTriple.relation.get(0).ner());
                        datas.add(selectedTriple.relationLemmaGloss());
                        datas.add(selectedTriple.object.get(0).ner());
                        datas.add(selectedTriple.objectLemmaGloss());
                        datas.add(String.valueOf(selectedTriple.confidence));

                        databaseConnection.prepareStatement(datas);
                    }
                }
            }
        }
        try {
            pipeline.shutdown();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void extractor(){
        Document doc = new Document("Lula was judge in Brazil. Mark work in Apple");

        for (Sentence sent : doc.sentences()){
            for (RelationTriple triple : sent.openieTriples()){
                //print the triple
                System.out.println(triple.confidence + "\t" +
                        triple.subjectLemmaGloss() + "\t" +
                        triple.relationLemmaGloss() + "\t" +
                        triple.objectLemmaGloss());
            }
        }
    }
}
