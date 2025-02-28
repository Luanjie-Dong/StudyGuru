package studyguru.backend.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import studyguru.backend.services.ChallengeGeneratorService;

@RestController
@RequestMapping("/challenges")
public class ChallengeController {

    @Autowired
    private ChallengeGeneratorService challengeGeneratorService;

    @PostMapping("/generateDailyChallenges")
    public void generateDailyChallengesForAllCourses() {
        System.out.println("Generating daily challenges for all courses");
        challengeGeneratorService.generateDailyChallengesForAllCourses();
    }

    @PostMapping("/generateCheckpointChallenges")
    public void generateCheckpointChallenges() {
        System.out.println("Generating checkpoint challenges");
        challengeGeneratorService.generateCheckpointChallenges();
    }
}