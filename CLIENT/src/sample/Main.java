package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
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

import java.awt.*;

public class Main extends Application {

    public Stage client_window;

    //scenes & layouts
    private Scene welcome_screen, menu_screen, textbook_screen,  barcode_screen;
    private BorderPane welcome_layout = new BorderPane(), menu_layout = new BorderPane();
    private VBox welcome_center = new VBox(), menu_center = new VBox();

    //Display values
    private String display_font = "Times New Roman";
    private int resolution_y = 500;
    private int resolution_x = 650;
    Status_boolean scanner = new Status_boolean();
    Status_boolean server = new Status_boolean();

    //check if screens have been made
    boolean textbook_made = false, barcode_made = false, help_made = false;

    public static void main(String[] args){
        launch(args);
    }

    //basically where the program starts
    @Override
    public void start(Stage primaryStage) throws Exception{
        //loading a bunch of stuff
        client_window = primaryStage;
        client_window.setTitle("DigiText");
        client_window.getIcons().add(new Image("/icons/sphs_icon.png"));

        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));

        /* Welcome Screen */
        //Welcome Label
        Label welcome_label = new Label("Welcome to DigiText! Press any key or the button to continue");
        welcome_label.setFont(Font.font(display_font, 20) );
        welcome_label.setTextFill(Color.color(0.69,0.19,0.38));

        //Welcome Button
        Button welcome_button = new Button("Press to continue");
        welcome_button.setOnAction(e-> menu());

        //Welcome Layout
        welcome_center.getChildren().addAll(welcome_label, welcome_button);
        welcome_center.setAlignment(Pos.CENTER);
        welcome_center.setSpacing(10);
        welcome_layout.setCenter(welcome_center);
        welcome_screen = new Scene(welcome_layout, resolution_x, resolution_y);
        welcome_screen.addEventHandler(KeyEvent.KEY_PRESSED, (key) -> {
            menu();
        });

        //keyboard testing stuff
        client_window.addEventHandler(KeyEvent.KEY_PRESSED, (key) -> {
            System.out.println("TEST: " + key);
            switch(key.getText()){
                //simulates barcode connection
                case "w":
                    scanner.setBool(true);
                    break;
                case "s":
                    scanner.setBool(false);
                    break;
                //simulates server connection
                case "q":
                    server.setBool(true);
                    break;
                case "a":
                    server.setBool(false);
                    break;
            }
        });

        //sets start screen as the welcome_screen
        client_window.setScene(welcome_screen);
        client_window.show();

        //scanner status


    }

    //Menu Screen
    private void menu(){

        /*Menu Buttons*/
        Button textbook_button = new Button("Textbook Management");
        textbook_button.setFont(Font.font(display_font, 15));
        textbook_button.setOnAction(e-> {
            if(check_scanner()){
                if(textbook_made){
                    client_window.setScene(textbook_screen);
                } else {
                    textbook_management();
                    textbook_made = true;
                }
            };
        });

        Button barcode_button = new Button("Barcode Maker / Textbook Scanner");
        barcode_button.setFont(Font.font(display_font, 15));

        Button help_button = new Button("Help");
        help_button.setFont(Font.font(display_font, 15));

        Button game_button = new Button("Bored?");
        game_button.setFont(Font.font(display_font, 5));
        game_button.setOnAction(e->AlertBox.display("ERROR","This feature is not complete yet!", "Close window"));


        menu_center.getChildren().addAll(textbook_button, barcode_button, help_button, game_button);
        menu_center.setAlignment(Pos.CENTER);
        menu_center.setSpacing(10);

        menu_layout.setCenter(menu_center);
        menu_screen = new Scene(menu_layout, resolution_x, resolution_y);
        client_window.setScene(menu_screen);

    }

    //checks if scanner is connected
    private boolean check_scanner(){
        if(scanner.getBool()){
            return true;
        } else{
            AlertBox.display("No Scanner Found", "Please connect a scanner and try again", "Got it Senpai!");
        }
        return false;
    }

    private void textbook_management(){

        VBox textbook_center = new VBox();
        GridPane textbook_left = new GridPane();
        HBox textbook_bottom = new HBox();
        BorderPane textbook_layout = new BorderPane();

        //bottom
        Button go_back = new Button("Back to menu");
        go_back.setOnAction(e-> {
            client_window.setScene(menu_screen);
        });
        textbook_bottom.getChildren().add(go_back);
        textbook_layout.setBottom(textbook_bottom);

        //center
        Label student_status = new Label("Please scan in a student's barcode");
        textbook_center.getChildren().add(student_status);
        textbook_center.setAlignment(Pos.CENTER);
        textbook_layout.setCenter(textbook_center);


        //top (status stuff)
        ImageView barcode_status_icon = scanner.getImageView();
        ImageView server_status_icon = server.getImageView();
        Label barcode_status_text = new Label("Barcode Scanner Status: ");
        Label server_status_text = new Label("Server Connected Status: ");
        textbook_left.add(barcode_status_text, 0, 0);
        textbook_left.add(barcode_status_icon, 1, 0);
        textbook_left.add(server_status_text, 0, 1);
        textbook_left.add(server_status_icon, 1, 1);
        textbook_layout.setTop(textbook_left);
        scanner.BoolProperty().addListener((v,oldValue, newValue) -> {
            barcode_status_icon.setImage(scanner.getImage());
        });
        server.BoolProperty().addListener((v,oldValue,newValue) -> {
           server_status_icon.setImage(server.getImage());
        });
        textbook_screen = new Scene(textbook_layout, resolution_x,resolution_y);
        client_window.setScene(textbook_screen);
    }
}
