import java.io.File;
import java.io.IOException;
import java.util.Scanner;


public class SmilesGrabber {


    private File[] files;
    private String[] smilesList;

    private SmilesFile[] processed;

    public SmilesGrabber(String dir, int smilesLine)
    {
        this.files = grabFiles(dir);
        this.processed = grabSmiles(smilesLine);

    }

    public File[] getFiles()
    {

        return this.files;
    }

    private File[] grabFiles(String dir)
    {
        File directory = new File(dir);
        File[] subFiles = directory.listFiles();
        return subFiles;
    }

    private SmilesFile[] grabSmiles(int smilesLine)
    {
        SmilesFile[] smilesList = new SmilesFile[files.length];
        int index = 0;
        for(File f: files)
        {
            try
            {
                Scanner scan = new Scanner(f);
                for(int i=0; i<smilesLine; i++)
                {
                    scan.nextLine();
                }
                String smiles = scan.nextLine();
                smiles = smiles.substring(8);
                smilesList[index++] = new SmilesFile(f,smiles);
            }
            catch(IOException e)
            {
                System.out.println("I don't care");
            }

        }

        return smilesList;
    }

    public static void main(String[] args)
    {
        String dir = "E:\\Development Project\\Data\\GNPS";
        int smilesLine = 7;
        SmilesGrabber grab = new SmilesGrabber(dir, smilesLine);
    }


    public SmilesFile[] getSmilesList() {
        return processed;
    }
}
