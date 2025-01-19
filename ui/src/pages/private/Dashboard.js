import React, { useState, useEffect } from 'react';
import { Container, Typography, Button, Box, Paper, Grid, Avatar, Divider, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import PrivateLayout from '../../components/layout/PrivateLayout';
import { AccountCircle, Chat as ChatIcon, Settings as SettingsIcon } from '@mui/icons-material';

const Dashboard = () => {
    const navigate = useNavigate();
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const token = localStorage.getItem('token');

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/v1/users/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch user data');
                }

                const data = await response.json();
                setUserData(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [token]);

    if (loading) {
        return (
            <PrivateLayout>
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                    <CircularProgress />
                </Box>
            </PrivateLayout>
        );
    }

    if (error) {
        return (
            <PrivateLayout>
                <Container>
                    <Typography color="error" align="center">
                        Error: {error}
                    </Typography>
                </Container>
            </PrivateLayout>
        );
    }

    return (
        <PrivateLayout>
            <Container maxWidth="lg">
                <Grid container spacing={3}>
                    {/* Welcome Section */}
                    <Grid item xs={12}>
                        <Paper elevation={3} sx={{ p: 3, mb: 3, bgcolor: 'primary.main', color: 'white' }}>
                            <Typography variant="h4" gutterBottom>
                                Welcome back, {userData?.full_name}! 👋
                            </Typography>
                            <Typography variant="subtitle1">
                                Ready to start your day with Albert AI?
                            </Typography>
                        </Paper>
                    </Grid>

                    {/* User Profile Card */}
                    <Grid item xs={12} md={4}>
                        <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
                            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
                                <Avatar sx={{ width: 80, height: 80, mb: 2, bgcolor: 'secondary.main' }}>
                                    <AccountCircle fontSize="large" />
                                </Avatar>
                                <Typography variant="h6" gutterBottom>
                                    {userData?.full_name}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    {userData?.email}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    ID: {userData?.id}
                                </Typography>
                                <Box sx={{ mt: 1 }}>
                                    <Typography variant="body2" color={userData?.is_active ? "success.main" : "error.main"}>
                                        Status: {userData?.is_active ? "Active" : "Inactive"}
                                    </Typography>
                                </Box>
                            </Box>
                            <Divider sx={{ my: 2 }} />
                            <Button
                                fullWidth
                                variant="outlined"
                                onClick={() => navigate('/profile')}
                                startIcon={<SettingsIcon />}
                            >
                                Edit Profile
                            </Button>
                        </Paper>
                    </Grid>

                    {/* Quick Actions */}
                    <Grid item xs={12} md={8}>
                        <Paper elevation={3} sx={{ p: 3, height: '100%' }}>
                            <Typography variant="h6" gutterBottom>
                                Quick Actions
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid item xs={12}>
                                    <Button
                                        fullWidth
                                        variant="contained"
                                        size="large"
                                        onClick={() => navigate('/chat')}
                                        startIcon={<ChatIcon />}
                                        sx={{ py: 2 }}
                                    >
                                        Start New Chat
                                    </Button>
                                </Grid>
                                {/* Add more quick actions here */}
                            </Grid>
                        </Paper>
                    </Grid>

                    {/* Recent Activity or Stats could go here */}
                    <Grid item xs={12}>
                        <Paper elevation={3} sx={{ p: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                Recent Activity
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                                Your recent interactions will appear here.
                            </Typography>
                        </Paper>
                    </Grid>
                </Grid>
            </Container>
        </PrivateLayout>
    );
};

export default Dashboard; 