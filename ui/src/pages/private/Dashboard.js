import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import PrivateLayout from '../../components/layout/PrivateLayout';

const Dashboard = () => {
    const navigate = useNavigate();
    const username = localStorage.getItem('username');

    return (
        <PrivateLayout>
            <Container maxWidth="md">
                <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h2" component="h1" gutterBottom>
                        Welcome back, {username}! 🚀
                    </Typography>
                    <Typography variant="h5" component="h2" gutterBottom color="text.secondary">
                        You're now connected to Albert AI
                    </Typography>
                    <Box sx={{ mt: 4 }}>
                        <Button
                            variant="contained"
                            color="primary"
                            size="large"
                            onClick={() => navigate('/chat')}
                            sx={{ mr: 2 }}
                        >
                            Start Chat
                        </Button>
                    </Box>
                </Box>
            </Container>
        </PrivateLayout>
    );
};

export default Dashboard; 