package studyguru.backend.models;

import java.util.ArrayList;

// import jakarta.persistence.Embeddable;
import studyguru.backend.enums.QuestionType;

// @Embeddable
public class QuestionDetail {
    private QuestionType question_type;
    private ArrayList<String> options;
    private String question;

    public QuestionDetail() {
    }

    public QuestionDetail(QuestionType question_type, ArrayList<String> options, String question) {
        this.question_type = question_type;
        this.options = options;
        this.question = question;
    }

    public QuestionType getQuestion_type() {
        return question_type;
    }

    public ArrayList<String> getOptions() {
        return options;
    }

    public String getQuestion() {
        return question;
    }

    
}
