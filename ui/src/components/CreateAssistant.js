const CreateAssistant = () => {
    const handleSubmit = async (values) => {
        try {
            const response = await api.post('/help-assistant', {
                ...values,
                tone: values.tone || 'PROFESSIONAL' // Default to professional if not selected
            });
            // Handle success
        } catch (error) {
            // Handle error
        }
    };

    return (
        <AssistantForm
            initialValues={{ tone: 'PROFESSIONAL' }}
            onSubmit={handleSubmit}
        />
    );
}; 