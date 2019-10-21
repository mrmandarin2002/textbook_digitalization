package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;

public class Main extends Application {

    Stage client_window;

    //scenes & layouts
    Scene welcome_screen, menu_screen;
    VBox welcome_layout;
    StackPane menu_layout;

    public static void main(String[] args){
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) throws Exception{
        client_window = primaryStage;
        Parent root = FXMLLoader.load(getClass().getResource("sample.fxml"));

        //welcome screen
        Label welcome_text = new Label("Welcome");
        Button click_to_continue = new Button("CLICK THIS TO CONTINUE");
        click_to_continue.setOnAction(e -> client_window.setScene(menu_screen));
        welcome_layout = new VBox(20);
        welcome_layout.getChildren().addAll(welcome_text, click_to_continue);

        welcome_screen = new Scene(welcome_layout, 500, 500);

        // menu //
        //menu buttons
        Button textbook_distribution = new Button("Textbook distribution");
        Button textbook_return = new Button("Textbook Return");
        Button instructions = new Button("Instructions");

        //menu layout
        menu_layout = new StackPane();
        menu_layout.getChildren().addAll(textbook_distribution, textbook_return, instructions);
        menu_screen = new Scene(menu_layout, 500, 500);

        client_window.setScene(welcome_screen);
        client_window.setTitle("SPHS Textbook Distribution");
        client_window.show();
    }

}
