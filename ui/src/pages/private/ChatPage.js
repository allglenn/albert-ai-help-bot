import React from 'react';
import { Container, Typography } from '@mui/material';
import PrivateLayout from '../../components/layout/PrivateLayout';

const ChatPage = () => {
    return (
        <PrivateLayout>
            <Container maxWidth="md">
                <Typography variant="h4" gutterBottom>
                    Chat with Albert AI
                </Typography>
                {/* Chat interface will go here */}
            </Container>
        </PrivateLayout>
    );
};

export default ChatPage; 