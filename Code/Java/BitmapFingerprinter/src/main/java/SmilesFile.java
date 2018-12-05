import java.io.File;

public class SmilesFile {

    private File f;
    private String smiles;

    public SmilesFile(File f, String smiles) {
        this.f = f;
        this.smiles = smiles;
    }

    public String getSmiles() {
        return smiles;
    }

    public void setSmiles(String smiles) {
        this.smiles = smiles;
    }

    public File getF() {
        return f;
    }

    public void setF(File f) {
        this.f = f;
    }
}
