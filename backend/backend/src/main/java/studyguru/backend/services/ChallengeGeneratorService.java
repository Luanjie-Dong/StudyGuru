package studyguru.backend.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import studyguru.backend.models.Checkpoint;
import studyguru.backend.models.Course;
import studyguru.backend.models.Module;
import studyguru.backend.enums.ChallengeType;
import studyguru.backend.models.ChallengeRequestDAO;
import studyguru.backend.services.CheckpointService;
import studyguru.backend.services.CourseService;
import studyguru.backend.services.ModuleService;

import java.time.LocalDate;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ChallengeGeneratorService {

    @Value("${llm.microservice.url}")
    private String llmMicroserviceUrl;

    private CourseService courseService;
    private CheckpointService checkpointService;
    private ModuleService moduleService;
    private RestTemplate restTemplate;

    public ChallengeGeneratorService(CourseService courseService, 
                                     CheckpointService checkpointService, 
                                     ModuleService moduleService, 
                                     RestTemplate restTemplate) {
        this.courseService = courseService;
        this.checkpointService = checkpointService;
        this.moduleService = moduleService;
        this.restTemplate = restTemplate;
    }

    @Scheduled(cron = "0 0 0 * * *") // Midnight
    public void generateDailyChallengesForAllCourses() {
        List<Course> courses = courseService.getAllCourses();
        for (Course course : courses) {
            generateDailyChallenge(course);
        }
    }

    @Scheduled(cron = "0 0 5 * * *") // 5 seconds after midnight, for improved efficiency
    public void generateCheckpointChallenges() {
        List<Checkpoint> checkpoints = checkpointService.getCheckpointsByDate(LocalDate.now().plusDays(3));
        for (Checkpoint checkpoint : checkpoints) {
            generateCheckpointChallenge(checkpoint.getCourse_id());
        }
    }

    private void generateDailyChallenge(Course course) {
        String latestModuleId = course.getLatest_module_id();
        List<String> modules = List.of(latestModuleId);
        ChallengeRequestDAO challengeRequest = new ChallengeRequestDAO(ChallengeType.DAILY, modules, course.getCourse_id());
        sendChallengeRequest(challengeRequest);
    }

    private void generateCheckpointChallenge(String course_id) {
        List<String> modules = moduleService.getModulesByCourseId(course_id) != null 
            ? moduleService.getModulesByCourseId(course_id)
                           .stream()
                           .map(m -> m.getModule_id())
                           .collect(Collectors.toList()) 
            : List.of();

        ChallengeRequestDAO challengeRequest = new ChallengeRequestDAO(ChallengeType.CHECKPOINT, modules, course_id);
        sendChallengeRequest(challengeRequest);
    }

    private void sendChallengeRequest(ChallengeRequestDAO challengeRequest) {
        restTemplate.postForObject(llmMicroserviceUrl, challengeRequest, Void.class);
    }
}
