package studyguru.backend.models;

import java.util.List;

import studyguru.backend.enums.ChallengeType;

public class ChallengeRequestDAO {
    private ChallengeType type;
    private List<String> modules;
    private String course_id;

    public ChallengeRequestDAO() {
    }
    
    public ChallengeRequestDAO(ChallengeType type, List<String> modules, String course_id) {
        this.type = type;
        this.modules = modules;
        this.course_id = course_id;
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

    
}
