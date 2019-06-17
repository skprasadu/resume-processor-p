package hw;

import java.io.*;
import java.nio.file.Files;
import javax.net.ssl.*;
import java.net.*;
import java.util.regex.*;
import java.util.ArrayList;

public class App {

  public static void main(String[] args) {

    if (args.length == 0) {
      System.out.println("Usage: java OCRestfulClient imageFileName");
      return;
    }

    final String baseUrl = System.getenv("OCRESTFUL_BASE_URL");
    final String secret = System.getenv("OCRESTFUL_API_SECRET");
    if (baseUrl == null || baseUrl.isEmpty() || secret == null || secret.isEmpty()) {
      System.out.println("You must import the OCRESTFUL environment variables OCRESTFUL_BASE_URL and OCRESTFUL_API_SECRET first");
      return;
    }

    Pattern rePattern = Pattern.compile("https?://([^/]+)/([a-zA-Z0-9]+)/");
    Matcher m = rePattern.matcher(baseUrl);
    String host = "";
    String clientID = "";
    if (m.find()) {
      host = m.group(1);
      clientID = m.group(2);
    } else {
      System.out.println("Hmmm. \"" + baseUrl + "\" doesn't look like a URL I can understand. Please check your OCRESTFUL_BASE_URL environment variable.");
      return;
    }

    int port = 443; // default https port
    String imageFileName = args[0];
    File file;
    long fileSize = 0;
    byte[] imageData = null;
    try {
      file = new File(imageFileName);
      if (!file.exists()) {
        System.out.println("Cannot find file " + imageFileName);
        return;
      }
      fileSize = file.length();
      imageData = Files.readAllBytes(file.toPath());
    } catch (IOException ex) {
    }

    String ext = imageFileName.toLowerCase().substring(imageFileName.lastIndexOf(".") + 1);
    String mimeType = (ext == "pdf")? "application/pdf": "image/" + ext;
    SSLSocketFactory factory = (SSLSocketFactory) SSLSocketFactory.getDefault();
    SSLSocket socket = null;
    try {
      socket = (SSLSocket) factory.createSocket(host, port);

      // enable all the suites
      String[] supported = socket.getSupportedCipherSuites();
      socket.setEnabledCipherSuites(supported);

      Writer out = new OutputStreamWriter(socket.getOutputStream(), "UTF-8");

      out.write("POST /" + clientID + "/res/ HTTP/1.1\r\n");
      out.write("Host: " + host + "\r\n");
      out.write("Content-Type: " + mimeType + "\r\n");
      out.write("Content-Length: " + fileSize + "\r\n");
      out.write("Secret: " + secret + "\r\n");
      out.write("\r\n");
      out.flush();

      socket.getOutputStream().write(imageData);
      socket.getOutputStream().flush();

      // read response
      BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

      // read the header
      String s;
      ArrayList<String> headers = new ArrayList<String>();
      while (!(s = in.readLine()).equals("")) {
        headers.add(s);
        if (s.startsWith("location:")) {
          System.out.println(headers.get(0));
          System.out.println("Your document can be found at: " + s.substring("location:".length()));
        }
      }
      /* You can parse the JSON body for additional URLs and URI templates, but that's an exercise for the reader. This sample ignores the body. */
    } catch (IOException ex) {
      System.err.println(ex);
    } finally {
        try {
          if (socket != null) socket.close();
        } catch (IOException e) {}
    }
  }
}
