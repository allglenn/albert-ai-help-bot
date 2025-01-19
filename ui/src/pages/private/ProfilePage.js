import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';
import PrivateLayout from '../../components/layout/PrivateLayout';

const ProfilePage = () => {
    const username = localStorage.getItem('username');

    return (
        <PrivateLayout>
            <Container maxWidth="md">
                <Paper elevation={3} sx={{ p: 4 }}>
                    <Typography variant="h4" gutterBottom>
                        Profile
                    </Typography>
                    <Box sx={{ mt: 2 }}>
                        <Typography variant="body1">
                            Email: {username}
                        </Typography>
                    </Box>
                </Paper>
            </Container>
        </PrivateLayout>
    );
};

export default ProfilePage; 