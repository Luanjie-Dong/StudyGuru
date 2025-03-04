package studyguru.backend.services;

import studyguru.backend.models.Checkpoint;
import studyguru.backend.models.Question;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
public class CheckpointService {

    @Value("$(checkpoint.microservice.url)")
    private String checkpointMicroserviceUrl;

    private RestTemplate restTemplate = new RestTemplate();

    public List<Checkpoint> getCheckpointsByDate(LocalDate date) {
        // Endpoint
        Checkpoint[] checkpoints = restTemplate.getForObject(checkpointMicroserviceUrl + "/checkpoint_date?date=" + date.toString(), Checkpoint[].class);
        return Arrays.asList(checkpoints);
    }
}
