import org.jsoup.*;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.*;

/**
 * Created by dell on 05/08/2017.
 */
public class FetchURLData {

    public String getData(String URL){
        StringBuilder text = new StringBuilder();
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
            Elements paragraphs = document.select("p");
            for (Element p : paragraphs){
                text.append(p.text().replaceAll("\\[\\d*\\d\\]", ""));
                text.append("\n");
            }
            //text = textFormat(document.body().text());

        } catch (MalformedURLException e){
            e.printStackTrace();
        } catch (IOException e){
            e.printStackTrace();
        }
        return text.toString();
    }

    /*
    Get the links of a web page removing ones that matches some args
     */
    public Set<String> getLinks(String URL, String[] args) throws IOException {
        Set<String> linkSet = new HashSet<String>();
        org.jsoup.nodes.Document document = Jsoup.connect(URL).get();
        Elements links = document.body().getElementsByTag("ul").select("li").select("a[href]");
                //getElementsByClass("wikitable").select("td:eq(0)").select("a[href]");

        /*
        Extract only name cites links, not geohack information
         */
        for (Element link : links){
            if(!containsArgs(link.attr("abs:href"), args) && containsArgs(link.attr("abs:href"), new String[]{"wikipedia"})) {
                linkSet.add(link.attr("abs:href"));
                //System.out.println("test");
            }
        }

        for (String link : linkSet){
            System.out.println(link);
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
        fetchURLData.getLinks("https://en.wikipedia.org/wiki/List_of_online_databases",
                new String[]{"https://tools.wmflabs.org/geohack/geohack", "List_of_online_databases", "index.php?", "Template", "Special", "Category", "Help", "Portal", "Wikipedia:"});

//        String text = fetchURLData.getData("https://en.wikipedia.org/wiki/Academia.edu");
//        System.out.println(text);

    }
}
