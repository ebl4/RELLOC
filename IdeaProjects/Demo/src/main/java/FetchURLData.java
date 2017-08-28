import org.jsoup.*;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

/**
 * Created by dell on 05/08/2017.
 */
public class FetchURLData {

    public String getData(String URL){
        String text = "";
        try {
            URL url = new URL(URL);
            BufferedReader br = new BufferedReader(new InputStreamReader(url.openStream()));
            String strTmp = "";
            StringBuilder rawHtml = new StringBuilder();
            while((strTmp = br.readLine()) != null){
                rawHtml.append(strTmp);
                rawHtml.append("\n");
            }

            org.jsoup.nodes.Document document = Jsoup.parse(rawHtml.toString());
            text = textFormat(document.body().text());

        } catch (MalformedURLException e){
            e.printStackTrace();
        } catch (IOException e){
            e.printStackTrace();
        }
        return text;
    }

    /*
    Get the links of a web page removing ones that matches some args
     */
    public Set<String> getLinks(String URL, String[] args) throws IOException {
        Set linkSet = new HashSet<String>();
        org.jsoup.nodes.Document document = Jsoup.connect(URL).get();
        Elements links = document.body().
                getElementsByClass("wikitable").select("a[href]");

        /*
        Extract only name cites links, not geohack information
         */
        for (Element link : links){
            if(!containsArgs(link.attr("abs:href"), args))
                linkSet.add(link.attr("abs:href") +" "+link.attr("rel"));
                //System.out.println(link.attr("abs:href") +" "+link.attr("rel"));
        }

        return linkSet;
    }

    public boolean containsArgs(String link, String[] args){
        for (String arg: args){
            if(link.contains(arg)){
                return true;
            }
        }
        return false;
    }

    public static String textFormat(String text){
        return text.replaceAll("[\\[[0-9]\\]]", "");
    }

    public static void main(String[] args) throws IOException {

        FetchURLData fetchURLData = new FetchURLData();
        //fetchURLData.getData("https://en.wikipedia.org/wiki/New_York_City");
        fetchURLData.getLinks("https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population",
                new String[]{"https://tools.wmflabs.org/geohack/geohack", "List_of_United_States_cities"});
    }
}
