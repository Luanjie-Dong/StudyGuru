package studyguru.backend.models;

import java.util.List;

import studyguru.backend.enums.ChallengeType;

public class QuestionsRequestDAO {
    private ChallengeType type;
    private List<String> modules;
    private String course_id;
    private String challenge_id;

    public QuestionsRequestDAO() {
    }
    
    public QuestionsRequestDAO(ChallengeType type, List<String> modules, String course_id, String challenge_id) {
        this.type = type;
        this.modules = modules;
        this.course_id = course_id;
        this.challenge_id = challenge_id;
    }

    public ChallengeType getType() {
        return type;
    }
    public List<String> getModules() {
        return modules;
    }
    public String getCourse_id() {
        return course_id;
    }
    public String getChallenge_id() {
        return challenge_id;
    }

    
}
