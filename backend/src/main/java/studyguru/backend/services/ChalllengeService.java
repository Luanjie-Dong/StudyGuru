package studyguru.backend.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import studyguru.backend.models.Challenge;
import studyguru.backend.models.ChallengeRequestDAO;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class ChalllengeService {

    @Value("$(challenge.microservice.url)")
    private String challengeMicroserviceUrl;
    
    private RestTemplate restTemplate = new RestTemplate();

    public Challenge createChallenge(ChallengeRequestDAO request) {
        ResponseEntity<Challenge> response = restTemplate.postForObject(challengeMicroserviceUrl + "/course", request, ResponseEntity.class);
        Challenge challenge = response.getBody();
        return challenge;
    }
    
}