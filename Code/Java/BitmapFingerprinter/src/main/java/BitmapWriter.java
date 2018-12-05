import org.openscience.cdk.exception.CDKException;
import org.openscience.cdk.exception.InvalidSmilesException;
import org.openscience.cdk.fingerprint.IBitFingerprint;
import org.openscience.cdk.fingerprint.SubstructureFingerprinter;
import org.openscience.cdk.interfaces.IAtomContainer;
import org.openscience.cdk.silent.SilentChemObjectBuilder;
import org.openscience.cdk.smiles.SmilesParser;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class BitmapWriter {

    private SmilesFile[] smilesList;
    private StringBuilder sb = new StringBuilder();

    public BitmapWriter(SmilesFile[] smilesList)
    {
        this.smilesList = smilesList;
    }

    public void writeBitmap()
    {
        SmilesParser sp = new SmilesParser(SilentChemObjectBuilder.getInstance());
        SubstructureFingerprinter fp = new SubstructureFingerprinter();
        ArrayList<String> invalidSmiles = new ArrayList<String>();
        ArrayList<String> cdkException = new ArrayList<String>();
        ArrayList<String> missingEntries = new ArrayList<String>();
        int count = 0;

        for(SmilesFile smiles: smilesList)
        {
            IAtomContainer mol = null;
            String fileEnd = smiles.getF().getName().replaceAll(".ms", "");
            try
            {
                mol = sp.parseSmiles(smiles.getSmiles());
                System.out.println(smiles.getSmiles());
                IBitFingerprint bfp = fp.getBitFingerprint(mol);
                count += 1;
                boolean has_entry = false;

                for(int i = 0; i<bfp.size(); i++)
                {
                    boolean currentBit = bfp.get(i);
                    if(currentBit){
                        has_entry = true;
                        sb.append(fileEnd).append(" ").append(i).append(" 1").append(System.getProperty("line.separator"));
                    }
                }
                if (!has_entry){
                    missingEntries.add(fileEnd);
                }
            }
            catch(InvalidSmilesException e)
            {
                invalidSmiles.add(fileEnd);
            } catch (CDKException e) {
                System.err.println("CDK Exception");
                cdkException.add(fileEnd);
            }

        }

        try
        {
            String filename = "G:/Dev/Data/For Family/GNPS Python Master/Final Fingerprints.txt";
            FileWriter writer = new FileWriter(filename);

            writer.write(sb.toString());
            writer.close();
            System.out.println(invalidSmiles);
            System.out.println(invalidSmiles.size());
            System.out.println(cdkException);
            System.out.println(cdkException.size());
            System.out.println(missingEntries);
            System.out.println(missingEntries.size());
            System.out.println(smilesList.length);
            System.out.println(count);

        }
        catch(IOException e)
        {
            e.printStackTrace();
            System.err.println("IOException");
        }
    }
}
