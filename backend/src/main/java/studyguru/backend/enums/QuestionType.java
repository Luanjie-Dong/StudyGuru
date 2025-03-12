package studyguru.backend.enums;

import com.fasterxml.jackson.annotation.JsonCreator;

public enum QuestionType {
    MCQ,
    MULTI_SELECT,
    SHORT_ANSWER;

    @JsonCreator
    public static QuestionType fromString(String value) {
        if (value == null) {
            return null;
        }
        String formatted = value.trim().toUpperCase().replace("-", "_").replace(" ", "_");
        switch(formatted) {
            case "SHORTANSWER":
            case "SHORT_OPEN_ENDED":
            case "SHORT_ANSWER":
                return SHORT_ANSWER;
            case "MULTISELECT":
            case "MULTI_SELECT":
                return MULTI_SELECT;
            case "MCQ":
                return MCQ;
            default:
                throw new IllegalArgumentException("Unknown QuestionType: " + value);
        }
    }
}
