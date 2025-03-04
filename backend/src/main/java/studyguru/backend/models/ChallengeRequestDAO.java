package studyguru.backend.models;

import studyguru.backend.enums.ChallengeType;

public class ChallengeRequestDAO {
    private String course_id;
    private ChallengeType type;
    public ChallengeRequestDAO() {
    }
    public ChallengeRequestDAO(String course_id, ChallengeType type) {
        this.course_id = course_id;
        this.type = type;
    }
    public String getCourse_id() {
        return course_id;
    }
    public ChallengeType getType() {
        return type;
    }
    
}
