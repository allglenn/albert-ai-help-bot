const EditAssistant = ({ assistant }) => {
    const handleSubmit = async (values) => {
        try {
            const response = await api.put(`/help-assistant/${assistant.id}`, {
                ...values,
                tone: values.tone
            });
            // Handle success
        } catch (error) {
            // Handle error
        }
    };

    return (
        <AssistantForm
            initialValues={{
                ...assistant,
                tone: assistant.tone || 'PROFESSIONAL'
            }}
            onSubmit={handleSubmit}
        />
    );
}; 