package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.scene.text.TextAlignment;
import javafx.stage.Stage;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Button;
import javafx.scene.control.*;

import java.awt.*;

public class Main extends Application {

    public Stage client_window;

    //scenes & layouts
    private Scene welcome_screen, menu_screen, textbook_screen,  scanner_screen, barcode_screen;

    //Display values
    private String display_font = "Times New Roman";

    //resolution of the window
    private int resolution_y = 500, resolution_x = 600;

    //booleans that have properties (so they can be put into listeners)
    Status_boolean server = new Status_boolean();
    Status_boolean barcode_scanned = new Status_boolean();

    //string of the barcode that will be scanned (constantly being updated)
    private String barcode_string = "";

    //to get the last time in which a keyboard input was made
    private long previous_input_time = 0;
    //timer
    KTimer timer = new KTimer();

    //check if screens have been made
    boolean textbook_made = false, barcode_made = false, help_made = false, textbook_scanner_made = false;

    public static void main(String[] args){
        launch(args);
    }

    //basically where the program starts
    @Override
    public void start(Stage primaryStage) throws Exception{

        //start loads a bunch of stuff
        //loading a bunch of stuff
        client_window = primaryStage;
        client_window.setTitle("DigiText");
        client_window.getIcons().add(new Image("/icons/sphs_icon.png"));

        Node root = FXMLLoader.load(getClass().getResource("sample.fxml")); //no clue wtf this does

        //starts timer
        timer.startTimer(0);

        //keyboard and barcode input
        client_window.addEventHandler(KeyEvent.KEY_PRESSED, (key) -> {
            if((timer.getTime() - previous_input_time) >= 30){
                barcode_scanned.setBool(false);
                barcode_string = "";
            }
            previous_input_time = timer.getTime();
            barcode_string += key.getText();
            //System.out.println(key);
            switch(key.getText()){
                //simulates server connection
                case "q":
                    server.setBool(true);
                    break;
                case "a":
                    server.setBool(false);
                    break;
            }
            //this is to get barcode input
            if(barcode_string.length() >= 5 && key.getCode() == KeyCode.ENTER) {
                barcode_scanned.setBool(true);
            }
        });

        //scanner status
        setWelcome_screen();

    }

    //welcome screen
    private void setWelcome_screen(){

        BorderPane welcome_layout = new BorderPane();
        VBox welcome_center = new VBox();

        //Welcome Label
        Label welcome_label = new Label("Welcome to DigiText! Press any key or the button to continue");
        welcome_label.setFont(Font.font(display_font, 20) );
        welcome_label.setTextFill(Color.color(0.69,0.19,0.38));

        //Welcome Button
        Button welcome_button = new Button("Press to continue");welcome_button.setOnAction(e-> {
            setMenu();
        });
        welcome_button.setFocusTraversable(false);

        //Welcome Layout
        welcome_center.getChildren().addAll(welcome_label, welcome_button);
        welcome_center.setAlignment(Pos.CENTER);
        welcome_center.setSpacing(10);
        welcome_layout.setCenter(welcome_center);
        welcome_screen = new Scene(welcome_layout, resolution_x, resolution_y);

        client_window.setScene(welcome_screen);
        client_window.show();
    }

    //Menu Screen
    private void setMenu(){
        BorderPane menu_layout = new BorderPane();
        VBox menu_center = new VBox();

        /*Menu Buttons*/
        Button textbook_button = new Button("Textbook Management");
        textbook_button.setFont(Font.font(display_font, 15));
        textbook_button.setOnAction(e-> {
            if(textbook_made){
                client_window.setScene(textbook_screen);
            } else {
                textbook_management();
                textbook_made = true;
            };
        });
        textbook_button.setFocusTraversable(false);

        Button textbook_scanner_button = new Button("Textbook Scanner");
        textbook_scanner_button.setFont(Font.font(display_font, 15));
        textbook_scanner_button.setFocusTraversable(false);
        textbook_scanner_button.setOnAction(e-> {
            if(textbook_scanner_made){
                client_window.setScene(scanner_screen);
            } else{
                setScanner_screen();
                textbook_scanner_made = true;
            }
        });


        Button barcode_maker_button = new Button("Barcode Maker");
        barcode_maker_button.setFont(Font.font(display_font, 15));
        barcode_maker_button.setFocusTraversable(false);

        Button help_button = new Button("Help");
        help_button.setFont(Font.font(display_font, 15));
        help_button.setFocusTraversable(false);

        Button game_button = new Button("Bored?");
        game_button.setFont(Font.font(display_font, 5));
        game_button.setOnAction(e->AlertBox.display("ERROR","This feature is not complete yet!", "Close window"));
        game_button.setFocusTraversable(false);


        menu_center.getChildren().addAll(textbook_button, textbook_scanner_button, barcode_maker_button, help_button, game_button);
        menu_center.setAlignment(Pos.CENTER);
        menu_center.setSpacing(10);

        menu_layout.setCenter(menu_center);
        menu_screen = new Scene(menu_layout, resolution_x, resolution_y);
        client_window.setScene(menu_screen);

    }

    private void textbook_management(){

        VBox textbook_center = new VBox();
        GridPane textbook_left = new GridPane();
        HBox textbook_bottom = new HBox();
        BorderPane textbook_layout = new BorderPane();

        //adds back button
        textbook_bottom.getChildren().add(back_button("Back to menu"));
        textbook_layout.setBottom(textbook_bottom);

        //center
        Label student_status = new Label("Please scan in a student's barcode");
        String work_pls = "Please scan in a student's barcode";
        textbook_center.getChildren().add(student_status);
        textbook_center.setAlignment(Pos.CENTER);
        textbook_layout.setCenter(textbook_center);


        //top (status stuff)
        ImageView server_status_icon = server.getImageView();
        Label server_status_text = new Label("Server Connected Status: ");
        textbook_left.add(server_status_text, 0, 0);
        textbook_left.add(server_status_icon, 1, 0);
        textbook_layout.setTop(textbook_left);
        server.BoolProperty().addListener((v,oldValue,newValue) -> {
           server_status_icon.setImage(server.getImage());
        });
        barcode_scanned.BoolProperty().addListener((v, oldValue, newValue) -> {
           if(barcode_scanned.getBool()){
               student_status.setText(barcode_string);
           }
        });
        textbook_screen = new Scene(textbook_layout, resolution_x,resolution_y);
        client_window.setScene(textbook_screen);
    }

    private void setScanner_screen(){
        BorderPane scanner_layout = new BorderPane();
        VBox scanner_bottom = new VBox(), scanner_left = new VBox();
        HBox scanner_center = new HBox();

        //adds back button
        scanner_bottom.getChildren().add(back_button("Back to menu"));

        TextField title_field = new TextField("Title");
        Label title_label = new Label("Title of textbook: ");
        Label condition_label = new Label("Condition of textbook: ");

        scanner_layout.setLeft(scanner_left);
        scanner_layout.setBottom(scanner_bottom);

        ChoiceBox<String> condition_choice = new ChoiceBox<>();
        condition_choice.getItems().addAll("New", "Good", "Used", "Bad");
        scanner_left.getChildren().addAll(title_label, title_field, condition_label, condition_choice);
        scanner_left.setSpacing(10);

        scanner_screen = new Scene(scanner_layout, resolution_x, resolution_y);
        client_window.setScene(scanner_screen);

    }

    private Button back_button(String button_string){
        Button go_back = new Button(button_string);
        go_back.setFocusTraversable(false);
        go_back.setOnAction(e-> {
            client_window.setScene(menu_screen);
        });
        return go_back;
    }
}
