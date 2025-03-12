package studyguru.backend.models;

import java.util.ArrayList;

// import jakarta.persistence.Embeddable;
import studyguru.backend.enums.QuestionType;

// @Embeddable
public class QuestionDetail {
    private QuestionType type;
    private ArrayList<String> options;
    private String question;

    public QuestionDetail() {
    }

    public QuestionDetail(QuestionType type, ArrayList<String> options, String question) {
        this.type = type;
        this.options = options;
        this.question = question;
    }

    public QuestionType getType() {
        return type;
    }

    public ArrayList<String> getOptions() {
        return options;
    }

    public String getQuestion() {
        return question;
    }

    
}
