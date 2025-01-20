import React, { useState, useEffect } from 'react';
import {
    Container, Typography, Paper, Box, Button, Avatar,
    CircularProgress, Grid, IconButton, Link
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import PrivateLayout from '../../components/layout/PrivateLayout';
import {
    Chat as ChatIcon,
    Link as LinkIcon,
    Edit as EditIcon,
    ArrowBack as ArrowBackIcon
} from '@mui/icons-material';

const ShowAssistantPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [assistant, setAssistant] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const token = localStorage.getItem('token');

    useEffect(() => {
        const fetchAssistant = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/v1/help-assistant/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch assistant details');
                }

                const data = await response.json();
                setAssistant(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAssistant();
    }, [id, token]);

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
            <Container maxWidth="lg" sx={{ py: 4 }}>
                <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
                    <IconButton onClick={() => navigate('/dashboard')}>
                        <ArrowBackIcon />
                    </IconButton>
                    <Typography variant="h4">Assistant Details</Typography>
                </Box>

                <Paper elevation={3} sx={{ p: 4 }}>
                    <Grid container spacing={4}>
                        <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
                            <Avatar
                                src={assistant.operator_pic}
                                sx={{ width: 200, height: 200, mx: 'auto', mb: 2 }}
                            />
                            <Typography variant="h5" gutterBottom>
                                {assistant.operator_name}
                            </Typography>
                            <Button
                                variant="contained"
                                startIcon={<ChatIcon />}
                                size="large"
                                onClick={() => navigate(`/chat/${assistant.id}`)}
                                sx={{ mt: 2 }}
                            >
                                Start Chat
                            </Button>
                        </Grid>

                        <Grid item xs={12} md={8}>
                            <Box sx={{ mb: 3 }}>
                                <Typography variant="h6" gutterBottom>
                                    {assistant.name}
                                </Typography>
                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                                    <LinkIcon sx={{ mr: 1, fontSize: 16 }} />
                                    <Link href={assistant.url} target="_blank" rel="noopener">
                                        {assistant.url}
                                    </Link>
                                </Box>
                            </Box>

                            <Box sx={{ mb: 3 }}>
                                <Typography variant="h6" gutterBottom>
                                    Mission
                                </Typography>
                                <Typography>
                                    {assistant.mission}
                                </Typography>
                            </Box>

                            <Box sx={{ mb: 3 }}>
                                <Typography variant="h6" gutterBottom>
                                    Description
                                </Typography>
                                <Typography>
                                    {assistant.description}
                                </Typography>
                            </Box>

                            <Box>
                                <Typography variant="h6" gutterBottom>
                                    Authorizations
                                </Typography>
                                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                                    {assistant.authorizations.map((auth) => (
                                        <Box
                                            key={auth}
                                            sx={{
                                                px: 2,
                                                py: 0.5,
                                                borderRadius: 1,
                                                bgcolor: 'primary.light',
                                                color: 'primary.contrastText'
                                            }}
                                        >
                                            {auth}
                                        </Box>
                                    ))}
                                </Box>
                            </Box>
                        </Grid>
                    </Grid>
                </Paper>
            </Container>
        </PrivateLayout>
    );
};

export default ShowAssistantPage; 