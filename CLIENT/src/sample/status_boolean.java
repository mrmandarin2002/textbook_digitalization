package sample;

        import javafx.beans.property.BooleanProperty;
        import javafx.beans.property.SimpleBooleanProperty;

public class Status_boolean {
    private BooleanProperty Bool = new SimpleBooleanProperty(this, "Bool", false);

    public BooleanProperty BoolProperty(){
        return Bool;
    }

    public boolean getBool(){
        return Bool.get();
    }

    public void setBool(boolean BoolName){
        this.Bool.set(BoolName);
    }
}
