package studyguru.backend.services;

import studyguru.backend.models.Checkpoint;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class CheckpointService {

    @Value("$(checkpoint.microservice.url)")
    private String checkpointMicroserviceUrl;

    public List<Checkpoint> getCheckpointsByDate(LocalDate date) {
        LocalDateTime startOfDay = date.atStartOfDay();
        LocalDateTime endOfDay = date.atTime(LocalTime.MAX);
        // Endpoint
        return new ArrayList<Checkpoint>();
    }
}
