import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;


public class SmilesGrabberForSingleFile {


    private Path path;
    private String[] smilesList;

    private ArrayList<Smiles> processed;

    public SmilesGrabberForSingleFile(String filename)
    {
        this.path = grabPath(filename);
        this.processed = grabSmilesFromOneFileNotEachLine();

    }

    public Path getPath()
    {
        return this.path;
    }


    private Path grabPath(String filename)
    {
        return Paths.get(filename);
    }

	
	private ArrayList<Smiles>  grabSmilesFromOneFile()
    {
        ArrayList<Smiles> smilesList = new ArrayList<Smiles>();

        try (Stream<String> lines = Files.lines(path, StandardCharsets.UTF_8).skip(1)) { // skip the first line of headers
            lines.forEachOrdered(line -> smilesList.add(new Smiles(line.split("\t")[0], line.split("\t")[1])));
        } catch (IOException e) {
            System.out.println("I don't care");
        }

        return smilesList;
    }

    private ArrayList<Smiles> grabSmilesFromOneFileNotEachLine()
    {
        ArrayList<Smiles> smilesList = new ArrayList<Smiles>();
        List<String> lines = new ArrayList<String>();
        boolean test = false;
        int count = 0;

        try {
            lines = Files.readAllLines(path, Charset.defaultCharset());
        } catch (IOException e) {
            e.printStackTrace();
        }

        for(String line : lines){
            if (line.startsWith("SMILES")){
                if (!line.substring(7).equals("N/A") && !line.substring(7).equals(" ") && !line.substring(7).equals("")){
                    String smiles = line.substring(7);
                    int spectrumIdIndex = count + 6;
                    String spectrumId = lines.get(spectrumIdIndex);
                    String id = spectrumId.split("=")[1];

                    smilesList.add(new Smiles(id, smiles));
                }
            }
            count += 1;
        }
        return smilesList;
    }

    public static void main(String[] args)
    {
        String filename = "G:\\Dev\\Data\\ALL_GNPS_20181012.mgf";
        SmilesGrabberForSingleFile grab = new SmilesGrabberForSingleFile(filename);
        grab.grabSmilesFromOneFileNotEachLine();
        //System.out.println(grab.grabSmilesFromOneFileNotEachLine().get(0));
    }


    public ArrayList<Smiles> getSmilesList() {
        return processed;
    }
}
