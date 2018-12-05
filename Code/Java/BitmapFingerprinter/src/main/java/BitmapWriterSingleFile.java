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

public class BitmapWriterSingleFile {

    private ArrayList<Smiles> smilesList;
    private StringBuilder sb = new StringBuilder();

    public BitmapWriterSingleFile(ArrayList<Smiles> smilesList)
    {
        this.smilesList = smilesList;
    }

    public void writeBitmap()
    {
        SmilesParser sp = new SmilesParser(SilentChemObjectBuilder.getInstance());
        SubstructureFingerprinter fp = new SubstructureFingerprinter();

        for(Smiles smiles: smilesList)
        {
            System.out.println(smiles.getSmiles());
            IAtomContainer mol = null;

            try
            {
                mol = sp.parseSmiles(smiles.getSmiles());
                IBitFingerprint bfp = fp.getBitFingerprint(mol);

                for(int i = 0; i<bfp.size(); i++)
                {
                    boolean currentBit = bfp.get(i);
                    if(currentBit){
                        sb.append(smiles.getID()).append(" ").append(i).append(" 1").append(System.getProperty("line.separator"));
                    }
                }
            }
            catch(InvalidSmilesException e)
            {
                System.out.println(smiles.getSmiles());
            } catch (CDKException e)
            {
                System.err.println("CDK Exception");
            }
        }

        try
        {
            String filename = "G:/Dev/Data/Fingerprint Bitmaps 2/";
            filename = filename + "ALL GNPS Final Fingerprints.txt";
            FileWriter writer = new FileWriter(filename);

            writer.write(sb.toString());
            writer.close();
        }
        catch(IOException e)
        {
            e.printStackTrace();
            System.err.println("IOException");
        }
    }

    public void test()
    {
        SmilesParser sp = new SmilesParser(SilentChemObjectBuilder.getInstance());
        SubstructureFingerprinter fp = new SubstructureFingerprinter();
        IAtomContainer mol = null;
        String smiles = "CC[C@H](C)[C@H]1C(=O)NC(=C)C(=O)N[C@H](C(=O)N[C@@H](CSC[C@H](C(=O)N1)NC(=O)/C(=C/C)/NC(=O)[C@H]([C@@H](C)CC)N)C(=O)N[C@@H]2[C@@H](SC[C@H](NC(=O)CNC(=O)[C@@H]3CCCN3C2=O)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H]4[C@@H](SC[C@H](NC(=O)CNC(=O)[C@@H](NC(=O)[C@@H](NC(=O)[C@@H](NC(=O)CNC4=O)C)CC(C)C)CCSC)C(=O)N[C@@H](CC(=O)N)C(=O)N[C@@H](CCSC)C(=O)N[C@@H](CCCCN)C(=O)N[C@@H]5[C@@H](SC[C@H]6C(=O)N[C@H](C(=O)N[C@@H](CS[C@H]([C@@H](CNC(=O)[C@@H](NC5=O)C)C(=O)N6)C)C(=O)N[C@@H](CO)C(=O)N[C@@H]([C@@H](C)CC)C(=O)N[C@@H](Cc7c[nH]cn7)C(=O)N[C@@H](C(C)C)C(=O)NC(=C)C(=O)N[C@@H](CCCCN)C(=O)O)Cc8cnc[nH]8)C)C)C)CC(C)C";
        try
        {
            mol = sp.parseSmiles(smiles);
            IBitFingerprint bfp = fp.getBitFingerprint(mol);
            for(int i = 0; i<bfp.size(); i++)
            {
                boolean currentBit = bfp.get(i);
                if(currentBit){
                    System.out.println(i);
                }
            }
        }
        catch(InvalidSmilesException e)
        {
            System.out.println(smiles);

        } catch (CDKException e)
        {
            System.err.println("CDK Exception");
        }
    }

}
