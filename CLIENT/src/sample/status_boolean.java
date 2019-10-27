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
        //System.out.println(this.getClass().getSimpleName() + " is set to " + BoolName);
        this.Bool.set(BoolName);
    }

    public void flipBool(){
        this.Bool.set(!Bool.get());
        System.out.println(this.getClass().getSimpleName() + " is now set to " + Bool.get());
    }
}
