export const getTones = async () => {
    const response = await api.get('/api/v1/help-assistant/tones');
    return response.data;
}; 