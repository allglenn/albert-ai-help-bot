import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import PublicLayout from '../../components/layout/PublicLayout';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <PublicLayout>
            <Container maxWidth="md">
                <Box sx={{ textAlign: 'center' }}>
                    <Typography variant="h2" component="h1" gutterBottom>
                        Welcome to Albert AI Demo integration project
                    </Typography>
                    <Typography variant="h5" component="h2" gutterBottom color="text.secondary">
                        Your AI-powered assistant for public services
                    </Typography>
                    <Box sx={{ mt: 4 }}>
                        <Button
                            variant="contained"
                            color="primary"
                            size="large"
                            onClick={() => navigate('/login')}
                            sx={{ mr: 2 }}
                        >
                            Login
                        </Button>
                        <Button
                            variant="outlined"
                            color="primary"
                            size="large"
                            onClick={() => navigate('/register')}
                        >
                            Register
                        </Button>
                    </Box>
                </Box>
            </Container>
        </PublicLayout>
    );
};

export default LandingPage; 