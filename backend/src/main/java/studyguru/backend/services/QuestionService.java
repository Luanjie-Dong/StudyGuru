package studyguru.backend.services;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import studyguru.backend.models.Question;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

@Service
public class QuestionService {

    @Value("${questions.microservice.url}")
    private String questionMicroserviceUrl;
    
    private RestTemplate restTemplate = new RestTemplate();
    private ObjectMapper objectMapper = new ObjectMapper();

    public void createQuestions(Question[] questions) {
        try {
            // Convert each Question to a Map, remove "question_id" field and collect
            List<Map<String,Object>> questionsList = new ArrayList<>();
            for (Question question : questions) {
                Map<String, Object> questionMap = objectMapper.convertValue(question, Map.class);
                questionMap.remove("question_id");
                questionsList.add(questionMap);
            }
            String jsonPayload = objectMapper.writeValueAsString(questionsList);
            System.out.println("JSON Payload without question_id: " + jsonPayload);
            
            // Post payload without question_id
            ResponseEntity<String> response = restTemplate.postForEntity(questionMicroserviceUrl + "/questions", questionsList, String.class);
            if (!response.getStatusCode().is2xxSuccessful()) {
                System.err.println("Failed to create questions");
            }
        } catch (Exception e) {
            System.err.println("Failed to convert questions to JSON");
        }
    }
}
