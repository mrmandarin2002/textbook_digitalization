package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.BorderPane;
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
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;

import java.awt.*;

public class Main extends Application {

    Stage client_window;

    //scenes & layouts
    Scene welcome_screen, menu_screen, textbook_distribution_screen, textbook_return_screen, barcode_screen;
    BorderPane welcome_layout = new BorderPane(), menu_layout = new BorderPane(), textbook_dis_layout = new BorderPane();
    VBox welcome_center = new VBox(), menu_center = new VBox();

    //Display values
    String display_font = "Times New Roman";
    int resolution_y = 500;
    int resolution_x = 650;
    boolean scanner_connected = true;

    public static void main(String[] args){
        launch(args);
    }

    //basically where the program starts
    @Override
    public void start(Stage primaryStage) throws Exception{
        client_window = primaryStage;
        client_window.setTitle("DigiText");
        client_window.getIcons().add(new Image(getClass().getResourceAsStream("sphs_icon.png")));

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
        welcome_screen.addEventHandler(KeyEvent.KEY_PRESSED, (key) -> menu());

        //sets start screen as the welcome_screen
        client_window.setScene(welcome_screen);
        client_window.show();

    }

    //Menu Screen
    private void menu(){

        /*Menu Buttons*/
        Button textbook_dis_button = new Button("Textbook Distribution");
        textbook_dis_button.setFont(Font.font(display_font, 15));
        textbook_dis_button.setOnAction(e-> {
            if(check_scanner()) textbook_distribution();
        });

        Button textbook_ret_button = new Button("Textbook Return");
        textbook_ret_button.setFont(Font.font(display_font, 15));

        Button barcode_button = new Button("Barcode Maker / Textbook Scanner");
        barcode_button.setFont(Font.font(display_font, 15));

        Button help_button = new Button("Help");
        help_button.setFont(Font.font(display_font, 15));

        Button game_button = new Button("Bored?");
        game_button.setFont(Font.font(display_font, 5));
        game_button.setOnAction(e->AlertBox.display("ERROR","This feature is not complete yet!", "Close window"));


        menu_center.getChildren().addAll(textbook_dis_button, textbook_ret_button, barcode_button, help_button, game_button);
        menu_center.setAlignment(Pos.CENTER);
        menu_center.setSpacing(10);

        menu_layout.setCenter(menu_center);
        menu_screen = new Scene(menu_layout, resolution_x, resolution_y);
        client_window.setScene(menu_screen);

    }
    //checks if scanner is connected
    private boolean check_scanner(){
        if(scanner_connected){
            return true;
        } else{
            AlertBox.display("No Scanner Found", "Please connect a scanner and try again", "Got it Senpai!");
        }
        return false;
    }

    private void textbook_distribution(){
        //buttons
        Button go_back = new Button("Back to menu");

    }
}
