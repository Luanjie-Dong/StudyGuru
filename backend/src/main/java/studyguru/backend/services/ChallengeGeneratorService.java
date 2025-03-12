package studyguru.backend.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import studyguru.backend.models.QuestionsRequestDAO;
import studyguru.backend.models.ChallengeRequestDAO;
import studyguru.backend.models.Challenge;
import studyguru.backend.models.Checkpoint;
import studyguru.backend.models.Course;
import studyguru.backend.models.Module;
import studyguru.backend.models.Question;
import studyguru.backend.enums.ChallengeType;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

import com.fasterxml.jackson.databind.ObjectMapper;

@Service
public class ChallengeGeneratorService {

    @Value("${llm.microservice.url}")
    private String llmMicroserviceUrl;

    @Autowired
    private CourseService courseService;

    @Autowired
    private CheckpointService checkpointService;

    @Autowired
    private ChalllengeService challlengeService;

    @Autowired
    private QuestionService questionService;

    @Autowired
    private ModuleService moduleService;

    private RestTemplate restTemplate = new RestTemplate();

    @Scheduled(cron = "0 0 0 * * *") // Midnight
    public void generateDailyChallengesForAllCourses() {
        System.out.println("LLM Microservice URL: " + llmMicroserviceUrl);
        List<Course> courses = courseService.getAllCourses();
        for (Course course : courses) {
            generateDailyChallenge(course);
        }
    }

    @Scheduled(cron = "0 0 5 * * *") // 5 seconds after midnight, for improved efficiency
    public void generateCheckpointChallenges() {
        System.out.println("LLM Microservice URL: " + llmMicroserviceUrl);
        List<Checkpoint> checkpoints = checkpointService.getCheckpointsByDate(LocalDate.now().plusDays(3));
        for (Checkpoint checkpoint : checkpoints) {
            generateCheckpointChallenge(checkpoint.getCourse_id());
        }
    }

    private void generateDailyChallenge(Course course) {
        String latestModuleId = course.getLatest_module_id();
        List<String> modules = List.of(latestModuleId);
        // Pre-generate challenge
        ChallengeRequestDAO challengeRequest = new ChallengeRequestDAO(course.getCourse_id(), ChallengeType.DAILY);
        Challenge newChallenge = challlengeService.createChallenge(challengeRequest);
        // Generate questions
        QuestionsRequestDAO questionsRequest = new QuestionsRequestDAO(ChallengeType.DAILY, modules, course.getCourse_id(), newChallenge.getChallenge_id());
        Question[] questions = generateQuestionsRequest(questionsRequest);

        questionService.createQuestions(questions);
    }

    private void generateCheckpointChallenge(String course_id) {
        List<String> modules = moduleService.getModulesByCourseId(course_id) != null 
            ? moduleService.getModulesByCourseId(course_id)
                           .stream()
                           .map(m -> m.getModule_id())
                           .collect(Collectors.toList()) 
            : List.of();

        // Pre-generate challenge
        ChallengeRequestDAO challengeRequest = new ChallengeRequestDAO(course_id, ChallengeType.CHECKPOINT);
        Challenge newChallenge = challlengeService.createChallenge(challengeRequest);
        // Generate questions
        QuestionsRequestDAO questionsRequest = new QuestionsRequestDAO(ChallengeType.CHECKPOINT, modules, course_id, newChallenge.getChallenge_id());
        Question[] questions = generateQuestionsRequest(questionsRequest);

        questionService.createQuestions(questions);
    }

    private Question[] generateQuestionsRequest(QuestionsRequestDAO questionsRequest) {
        ResponseEntity<String> responseEntity = restTemplate.postForEntity(llmMicroserviceUrl + "/generate_question", questionsRequest, String.class);
        String responseBody = responseEntity.getBody();
        // System.out.println("Raw response: " + responseBody);
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            return objectMapper.readValue(responseBody, Question[].class);
        } catch (Exception e) {
            throw new RuntimeException("Failed to deserialize response", e);
        }
    }
}
