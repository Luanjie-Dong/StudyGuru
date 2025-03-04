package studyguru.backend.services;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import studyguru.backend.models.Question;

import java.util.Arrays;

@Service
public class QuestionService {

    @Value("$(question.microservice.url)")
    private String questionMicroserviceUrl;
    
    private RestTemplate restTemplate;

    public void createQuestions(Question[] questions) {
        ResponseEntity<String> response = restTemplate.postForEntity(questionMicroserviceUrl + "/questions", questions, String.class);
        if (!response.getStatusCode().is2xxSuccessful()) {
            System.err.println("Failed to create questions");
        }
    }
}
