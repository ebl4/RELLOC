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

import java.util.*;
import java.util.stream.Collectors;

/**
 * Created by dell on 14/03/2017.
 */
public class CoreDemo {
    public static void main(String[] args) {
        DatabaseConnection databaseConnection = new DatabaseConnection();

        System.out.println("test");

        long start = System.currentTimeMillis();

        // read some text in the text variable
        String text = "Obama lives in Washington.";
        text = "New York City is also the most densely populated major city in the United States";
        FetchURLData fetchURLData = new FetchURLData();
        //text = fetchURLData.getData("https://en.wikipedia.org/wiki/New_York_City");

        //run annotation relation extractor (openie)
        //annotation_extractor(text);

        annotation_extractor(text.split("\\."), databaseConnection);

        long end = System.currentTimeMillis();

        System.out.println("Time: "+(end - start));

    }


    public static void process_sentences_core(String text){
        int contSent = 0, contRel = 0;
        DatabaseConnection databaseConnection = new DatabaseConnection();
        Properties props = new Properties();

        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, relation");
        StanfordCoreNLPClient pipeline = new StanfordCoreNLPClient(props, "localhost", 9000, 10);

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

                System.out.printf("Analysing sentence %d\n", +contSent++);
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
                        .filter( triple ->
                                triple.subject.stream().noneMatch(token -> "O".equals(token.ner())))
                        // make sure the object is entirely named entities
                        .filter( triple ->
                                triple.object.stream().noneMatch(token -> "O".equals(token.ner())))
                        // Convert the stream back to a list
                        .collect(Collectors.toList());

                int count = 0;
                for (RelationTriple triple : withNE) {
                    datas.clear();
                    /*List<CoreLabel> tokens = triple.allTokens();

                    for (CoreLabel token : tokens){
                        System.out.println(token);
                        System.out.println(token.get(CoreAnnotations.NamedEntityTagAnnotation.class));
                    }*/

                    System.out.printf("Triple %d\n", ++count);
                    datas.add(triple.subject.get(0).ner());
                    datas.add(triple.subjectLemmaGloss());
                    datas.add(triple.relation.get(0).ner());
                    datas.add(triple.relationLemmaGloss());
                    datas.add(triple.object.get(0).ner());
                    datas.add(triple.objectLemmaGloss());
                    datas.add(String.valueOf(triple.confidence));

                    databaseConnection.prepareStatement(datas);
                }
            }
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
