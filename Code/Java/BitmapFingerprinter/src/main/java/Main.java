public class Main {

    public static void main(String[] args)
    {
//        SmilesGrabberForSingleFile sg = new SmilesGrabberForSingleFile("G:/Dev/Data/ALL_GNPS_20181012.mgf");
//        BitmapWriterSingleFile bw = new BitmapWriterSingleFile(sg.getSmilesList());
        SmilesGrabber sg = new SmilesGrabber("G:/Dev/Data/GNPS For Family", 6);
        BitmapWriter bw = new BitmapWriter(sg.getSmilesList());

        bw.writeBitmap();
    }
}
