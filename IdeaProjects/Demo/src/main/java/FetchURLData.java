import org.jsoup.*;
import org.w3c.dom.Document;


import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;

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

    public static String textFormat(String text){
        return text.replaceAll("[\\[[0-9]\\]]", "");
    }

    public static void main(String[] args) {

        FetchURLData fetchURLData = new FetchURLData();
        fetchURLData.getData("https://en.wikipedia.org/wiki/New_York_City");
    }
}
