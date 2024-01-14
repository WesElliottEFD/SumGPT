# Core Business Logic (Entities)

The Core Business Logic of our application, which is focused on enhancing user engagement at events, is encapsulated in the Entities layer of our architecture. This layer is responsible for representing the domain models and their associated business rules. Below is an analysis of the data models and their functions within this layer.

## Data Models

### Event

- **Attributes:**
  - `eventId`: A unique identifier for the event.
  - `eventName`: The name of the event.
  - `eventDescription`: A detailed description of the event.
  - `startTime`: The scheduled start time of the event.
  - `endTime`: The scheduled end time of the event.
  - `location`: The physical or virtual location of the event.
- **Functions:**
  - `schedule()`: Sets the start and end time for the event.
  - `updateDetails()`: Updates the event's name and description.
  - `relocate()`: Changes the event's location.

### Participant

- **Attributes:**
  - `participantId`: A unique identifier for the participant.
  - `name`: The name of the participant.
  - `email`: The email address of the participant.
  - `registeredEvents`: A list of events the participant is registered for.
- **Functions:**
  - `registerForEvent(Event event)`: Registers the participant for a given event.
  - `unregisterFromEvent(Event event)`: Unregisters the participant from a given event.
  - `getRegisteredEvents()`: Returns a list of events the participant is registered for.

### EngagementMetric

- **Attributes:**
  - `metricId`: A unique identifier for the metric.
  - `participantId`: The identifier of the participant this metric is associated with.
  - `eventId`: The identifier of the event this metric is associated with.
  - `engagementScore`: A numerical value representing the participant's engagement.
- **Functions:**
  - `calculateScore()`: Calculates the engagement score based on participant's activity.
  - `updateScore(int newScore)`: Updates the engagement score with a new value.

## Shared Dependencies

- `DataModelSchemas`: The schemas for the above data models are used across the application to ensure data integrity and consistency.
- `BusinessLogicFunctions`: The functions associated with each data model are invoked by the Use Cases to perform operations on the data.
- `UseCaseDescriptions`: The business processes that involve these entities are detailed in the [UseCases.md](../Business Processes/UseCases.md) file.
- `TestingMethodNames`: The methods used to test these entities are described in the [TestingMethods.md](../Testing and Quality Assurance/TestingMethods.md) file.

## Conclusion

The Entities layer is crucial for maintaining the business logic of our application separate from other concerns. It is essential to ensure that these models accurately represent the domain and that their functions enforce the business rules effectively. As the application evolves, these models may need to be refactored or extended to accommodate new features or changes in business requirements.