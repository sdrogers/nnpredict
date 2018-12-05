public class Smiles {

    private String id;
    private String smiles;

    public Smiles(String id, String smiles) {
        this.id = id;
        this.smiles = smiles;
    }

    public String getSmiles() {
        return smiles;
    }

    public void setSmiles(String smiles) {
        this.smiles = smiles;
    }

    public String getID() {
        return id;
    }

    public void setID(String id) {
        this.id = id;
    }
}
