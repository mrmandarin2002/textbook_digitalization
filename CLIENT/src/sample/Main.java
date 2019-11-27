package sample;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.*;

import java.io.IOException;

public class Main extends Application {

    private Stage client_window;

    //all the commands to send and receive information from the server
    private Interaction server = new Interaction("127.0.0.1", 7356);

    private Scene menu_screen, barcode_screen;

    //Display values
    private String display_font = "Times New Roman";

    //resolution of the window
    private int resolution_y = 500, resolution_x = 600;

    //booleans that have properties (so they can be put into listeners)
    private Status_boolean barcode_scanned = new Status_boolean();

    //string of the barcode that will be scanned (constantly being updated)
    private String barcode_string = "";

    //to get the last time in which a keyboard input was made
    private long previous_input_time = 0;

    //timer to see if keyboard input was actually barcode input
    private KTimer timer = new KTimer();



    public Main() throws IOException {
    }

    public static void main(String[] args) {
        launch(args);
    }

    //basically where the program starts
    @Override
    public void start(Stage primaryStage) {

        //start loads a bunch of stuff
        //loading a bunch of stuff
        client_window = primaryStage;
        client_window.setTitle("DigiText");
        client_window.getIcons().add(new Image("/icons/sphs_icon.png"));
        barcode_scanned.setBool(false);

        //starts timer
        timer.startTimer(0);

        //keyboard and barcode input
        client_window.addEventHandler(KeyEvent.KEY_PRESSED, (key) -> {
            if((timer.getTime() - previous_input_time) >= 30){
                barcode_scanned.setBool(false);
                barcode_string = "";
            }
            previous_input_time = timer.getTime();
            if(key.getCode() != KeyCode.ENTER) {
                barcode_string += key.getText();
            }
            //this is to get barcode input
            if(barcode_string.length() >= 5 && key.getCode() == KeyCode.ENTER) {
                barcode_scanned.setBool(true);
            }
        });
        //after initialization of everything, go to the welcome screen
        setWelcome_screen();
    }

    //welcome screen
    private void setWelcome_screen() {

        //panes of the scene
        BorderPane welcome_layout = new BorderPane();
        VBox welcome_center = new VBox();

        //Welcome Label
        Label welcome_label = new Label("Welcome to DigiText! Press any key or the button to continue");
        welcome_label.setFont(Font.font(display_font, 20) );
        welcome_label.setTextFill(Color.color(0.69,0.19,0.38));

        //Welcome Button
        Button welcome_button = new Button("Press to continue");
        welcome_button.setOnAction(e-> { setMenu();});
        welcome_button.setFocusTraversable(false);

        //Welcome Layout
        welcome_center.getChildren().addAll(welcome_label, welcome_button);
        welcome_center.setAlignment(Pos.CENTER);
        welcome_center.setSpacing(10);
        welcome_layout.setCenter(welcome_center);
        //scenes & layouts
        Scene welcome_screen = new Scene(welcome_layout, resolution_x, resolution_y);

        client_window.setScene(welcome_screen);
        client_window.show();
    }

    //Menu Screen
    private void setMenu()  {
        BorderPane menu_layout = new BorderPane();
        VBox menu_center = new VBox();

        /*Menu Buttons*/
        Button textbook_button = new Button("Textbook Management");
        textbook_button.setFont(Font.font(display_font, 15));
        textbook_button.setOnAction(e-> {
            textbook_management();
        });
        textbook_button.setFocusTraversable(false);

        Button textbook_scanner_button = new Button("Textbook Scanner");
        textbook_scanner_button.setFont(Font.font(display_font, 15));
        textbook_scanner_button.setFocusTraversable(false);
        textbook_scanner_button.setOnAction(e-> {
            setScanner_screen();
        });

        Button help_button = new Button("Help");
        help_button.setFont(Font.font(display_font, 15));
        help_button.setFocusTraversable(false);

        Button game_button = new Button("Bored?");
        game_button.setFont(Font.font(display_font, 5));
        game_button.setOnAction(e->AlertBox.display("ERROR","This feature is not complete yet!", "Close window"));
        game_button.setFocusTraversable(false);


        menu_center.getChildren().addAll(textbook_button, textbook_scanner_button, help_button, game_button);
        menu_center.setAlignment(Pos.CENTER);
        menu_center.setSpacing(10);

        menu_layout.setCenter(menu_center);
        menu_screen = new Scene(menu_layout, resolution_x, resolution_y);
        client_window.setScene(menu_screen);

    }

    private void textbook_management() {

        VBox textbook_center = new VBox();
        GridPane textbook_left = new GridPane();
        HBox textbook_bottom = new HBox();
        BorderPane textbook_layout = new BorderPane();

        Boolean student_info_in[] = {false};
        String student_info[] = {""};

        //adds back button
        textbook_bottom.getChildren().add(back_button("Back to menu"));
        textbook_layout.setBottom(textbook_bottom);

        //center
        Label student_status = new Label("Please scan in a student's barcode");
        String work_pls = "Please scan in a student's barcode";
        textbook_center.getChildren().add(student_status);
        textbook_center.setAlignment(Pos.CENTER);
        textbook_layout.setCenter(textbook_center);

        // ***************** WORK IN PROGRESS ************************
        barcode_scanned.BoolProperty().addListener((v, oldValue, newValue) -> {
           if(barcode_scanned.getBool()){
               try {
                   if(server.valid_s(barcode_string)){
                        student_status.setText("");
                        student_info_in[0] = true;

                   } else if (server.valid_t(barcode_string)){
                        if(student_info_in[0]){
                            student_info[0] = server.info_s(barcode_string);
                        } else{
                            AlertBox.display("Error", "You need to scan in a student's barcode first before you can start scanning in textbook!", "Of course senpai");
                        }
                   } else{
                       if(student_info_in[0]){
                            AlertBox.display("Error", "This student / textbook's barcode was not recognized", "Got it senpai!");
                       } else{
                            AlertBox.display("Error", "This student's barcode was not recognized", "Got it senpai!");
                       }
                   }
               } catch (IOException e) {
                   e.printStackTrace();
               }
           }
        });
        Scene textbook_screen = new Scene(textbook_layout, resolution_x, resolution_y);
        client_window.setScene(textbook_screen);
    }

    private void setScanner_screen() {

        int[] num_of_textbooks_scanned = {0};
        Boolean[] values_set = {false};
        BorderPane scanner_layout = new BorderPane();
        VBox scanner_bottom = new VBox(), scanner_left = new VBox(), scanner_center = new VBox();
        GridPane scanner_top = new GridPane();

        //adds back button
        scanner_bottom.getChildren().add(back_button("Back to menu"));

        TextField title_field = new TextField("Title");
        TextField price_field = new TextField("Price");

        Label title_label = new Label("Title of textbook: ");
        title_label.setFont(Font.font(display_font, FontWeight.BOLD, 15));
        Label condition_label = new Label("Condition of textbook: ");
        condition_label.setFont(Font.font(display_font, FontWeight.BOLD, 15));
        Label price_label = new Label("Price of textbook:");
        price_label.setFont(Font.font(display_font, FontWeight.BOLD, 15));

        Label textbook_num_label = new Label("Number of current textbook scanned: " + num_of_textbooks_scanned[0]);
        Label barcode_label = new Label("Current barcode ID: " + barcode_string);
        scanner_center.getChildren().addAll(textbook_num_label, barcode_label);
        scanner_center.setAlignment(Pos.CENTER);
        scanner_layout.setCenter(scanner_center);

        Button set_button = new Button("Set textbook values");
        set_button.setFocusTraversable(false);
        set_button.setOnAction(e->{
            values_set[0] = !values_set[0];
            System.out.println(price_field.getText());
            if(values_set[0]){
                if(price_check(price_field.getText())) {
                    title_field.setDisable(true);
                    price_field.setDisable(true);
                    set_button.setText("Reset");
                }
                else{
                    values_set[0] = !values_set[0];
                    AlertBox.display("Idiot.", "Please stop trying to break my program and enter a number in the textfield", "I'll stop being stupid from now on!");
                }

            }
            else{
                title_field.setDisable(false);
                price_field.setDisable(false);
                set_button.setText("Set textbook values");
                num_of_textbooks_scanned[0] = 0;
                textbook_num_label.setText("Number of current textbook scanned: " + num_of_textbooks_scanned[0]);
                barcode_string = "";
                barcode_label.setText("Current barcode ID: " + barcode_string);
            }
        });


        ChoiceBox<String> condition_choice = new ChoiceBox<>();
        condition_choice.getItems().addAll("New", "Good", "Used", "Bad");
        condition_choice.setValue("New");
        scanner_left.getChildren().addAll(title_label, title_field, condition_label, condition_choice, price_label, price_field, set_button);
        scanner_left.setSpacing(6);
        scanner_left.setPadding(new Insets(10,0,0,10));
        scanner_left.setAlignment(Pos.CENTER);

        //if a barcode gets scanned in
        barcode_scanned.BoolProperty().addListener((v, oldValue, newValue) -> {
            if(barcode_scanned.getBool() && values_set[0]){
                try {
                    if(server.ping()) {
                        if(server.valid_s(barcode_string)){
                            AlertBox.display("Error", "This is a student's barcode dumbo!", "YIKES!");
                        }
                        else{
                            boolean addTextbook = true;
                            String textbook_info = "";
                            if(server.valid_t(barcode_string)){

                                addTextbook = OptionBox.display("Replace?", "This textbook was found in the database, would you like to replace it?");
                                if(addTextbook){
                                    server.delete_t(barcode_string);
                                }
                            }
                            if(addTextbook) {
                                num_of_textbooks_scanned[0]++;
                                String textbook_title = title_field.getText();
                                double textbook_price = Double.parseDouble(price_field.getText());
                                String textbook_condition = condition_choice.getValue();
                                textbook_num_label.setText("Number of current textbook scanned: " + num_of_textbooks_scanned[0]);
                                barcode_label.setText("Current barcode ID: " + barcode_string);
                                server.add_t(barcode_string, textbook_title, Double.toString(textbook_price), Integer.toString(condition_return(textbook_condition)));
                            }
                        }
                    } else{
                        AlertBox.display("Error", "You are not connected to the server idiot", "Maybe turn on your wifi?");
                    }
                } catch (IOException e) {
                    AlertBox.display("Error", "You are not connected to the server idiot", "Maybe turn on your wifi?");
                }
            } else if(!values_set[0]){
                AlertBox.display("Error", "Please care to click the set values button before scanning in stuff, dumbo", "Of course");
            }
        });

        scanner_layout.setLeft(scanner_left);
        scanner_layout.setBottom(scanner_bottom);

        Scene scanner_screen = new Scene(scanner_layout, resolution_x, resolution_y);
        client_window.setScene(scanner_screen);

    }

    private boolean price_check(String dubs){
        try{
            double price_dec = Double.parseDouble(dubs);
            return true;
        } catch(Exception e){
            return false;
        }
    }

    private Button back_button(String button_string){
        Button go_back = new Button(button_string);
        go_back.setFocusTraversable(false);
        go_back.setOnAction(e-> {
            client_window.setScene(menu_screen);
        });
        return go_back;
    }

    private int condition_return(String cond){
        switch(cond){
            case "New":
                return 0;
            case "Good":
                return 1;
            case "Used":
                return 2;
            case "Bad":
                return 3;
            default:
                return -1;
        }
    }
}
