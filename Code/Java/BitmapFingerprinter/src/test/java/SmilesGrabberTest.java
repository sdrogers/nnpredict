import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInstance;

import static org.junit.jupiter.api.Assertions.*;

@TestInstance(TestInstance.Lifecycle.PER_CLASS) class SmilesGrabberTest {

    private SmilesGrabber grabs;

    @BeforeAll
    public void setUp()
    {
        grabs = new SmilesGrabber("E:/Development Project/Data/GNPS", 6);
    }

    @Test
    public void correct_File_Amount()
    {
        int l = grabs.getFiles().length;
        int k = grabs.getSmilesList().length;
        assertEquals(5770, l, "Incorrect number of files grabbed");
        assertEquals(5770, k, "Incorrect number of smiles grabbed");
    }

    @Test
    public void correct_smiles_Format()
    {
        String smiles = grabs.getSmilesList()[0].getSmiles();
        String expectedSmiles = "O=C1OC(C(C)C(O)C(C)CCC)C(C)C(OC)CC2=NC(=CS2)C3=NC(C4=NC(C(O)=NC(C(O)C(C(=O)OC(C(O)=NC1C(O)C)C(C)CC)C)C(C)CC)(C)CS4)(C)CS3";
        assertEquals(expectedSmiles, smiles, "First smiles not correct");
        smiles = grabs.getSmilesList()[1].getSmiles();
        expectedSmiles = "O=C1CCC(O)C2OC12C(=CCl)CN=C(O)CCC=CCC(OC)CCCCCCC";
        assertEquals(expectedSmiles, smiles, "Second smiles not correct");
    }

}