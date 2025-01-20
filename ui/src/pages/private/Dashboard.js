import React, { useState, useEffect } from 'react';
import {
    Container, Typography, Button, Box, Paper, Grid, Avatar,
    Divider, CircularProgress, Dialog, DialogTitle, DialogContent,
    DialogActions, TextField, MenuItem, Card, CardContent, IconButton
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import PrivateLayout from '../../components/layout/PrivateLayout';
import {
    AccountCircle, Chat as ChatIcon, Settings as SettingsIcon,
    Add as AddIcon, Link as LinkIcon, Delete as DeleteIcon, Edit as EditIcon
} from '@mui/icons-material';

const Dashboard = () => {
    const navigate = useNavigate();
    const [userData, setUserData] = useState(null);
    const [assistants, setAssistants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [openDialog, setOpenDialog] = useState(false);
    const [deleteConfirmOpen, setDeleteConfirmOpen] = useState(false);
    const [selectedAssistant, setSelectedAssistant] = useState(null);
    const [updateDialog, setUpdateDialog] = useState(false);
    const [assistantToUpdate, setAssistantToUpdate] = useState(null);
    const token = localStorage.getItem('token');

    const [newAssistant, setNewAssistant] = useState({
        name: '',
        url: '',
        mission: '',
        description: '',
        operator_name: '',
        authorizations: []
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch user data
                const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!userResponse.ok) {
                    throw new Error('Failed to fetch user data');
                }

                const userData = await userResponse.json();
                setUserData(userData);

                // Fetch assistants
                const assistantsResponse = await fetch('http://localhost:8000/api/v1/help-assistant/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!assistantsResponse.ok) {
                    throw new Error('Failed to fetch assistants');
                }

                const assistantsData = await assistantsResponse.json();
                setAssistants(assistantsData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [token]);

    const handleCreateAssistant = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/v1/help-assistant/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newAssistant),
            });

            if (!response.ok) {
                throw new Error('Failed to create assistant');
            }

            const createdAssistant = await response.json();
            setAssistants([...assistants, createdAssistant]);
            setOpenDialog(false);
            setNewAssistant({
                name: '',
                url: '',
                mission: '',
                description: '',
                operator_name: '',
                authorizations: []
            });
        } catch (err) {
            setError(err.message);
        }
    };

    const handleDeleteAssistant = async () => {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/help-assistant/${selectedAssistant.id}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to delete assistant');
            }

            setAssistants(assistants.filter(a => a.id !== selectedAssistant.id));
            setDeleteConfirmOpen(false);
            setSelectedAssistant(null);
        } catch (err) {
            setError(err.message);
        }
    };

    const handleUpdateAssistant = async () => {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/help-assistant/${assistantToUpdate.id}`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(assistantToUpdate),
            });

            if (!response.ok) {
                throw new Error('Failed to update assistant');
            }

            const updatedAssistant = await response.json();
            setAssistants(assistants.map(a => a.id === updatedAssistant.id ? updatedAssistant : a));
            setUpdateDialog(false);
            setAssistantToUpdate(null);
        } catch (err) {
            setError(err.message);
        }
    };

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
                {/* Welcome Banner */}
                <Paper
                    elevation={3}
                    sx={{
                        p: 4,
                        mb: 4,
                        background: 'linear-gradient(45deg, #1976d2 30%, #2196f3 90%)',
                        color: 'white'
                    }}
                >
                    <Grid container alignItems="center" spacing={3}>
                        <Grid item xs={12} md={8}>
                            <Typography variant="h3" gutterBottom>
                                Welcome back, {userData?.full_name}! 👋
                            </Typography>
                            <Typography variant="h6" sx={{ opacity: 0.9 }}>
                                Your AI-powered assistants are ready to help
                            </Typography>
                        </Grid>
                        <Grid item xs={12} md={4} sx={{ textAlign: 'right' }}>
                            <Button
                                variant="contained"
                                color="secondary"
                                size="large"
                                startIcon={<AddIcon />}
                                onClick={() => setOpenDialog(true)}
                                sx={{
                                    bgcolor: 'white',
                                    color: 'primary.main',
                                    '&:hover': {
                                        bgcolor: 'rgba(255, 255, 255, 0.9)'
                                    }
                                }}
                            >
                                Add New Assistant
                            </Button>
                        </Grid>
                    </Grid>
                </Paper>

                <Grid container spacing={4}>
                    {/* User Profile Section */}
                    <Grid item xs={12} md={4}>
                        <Card elevation={3}>
                            <CardContent>
                                <Box sx={{ textAlign: 'center', mb: 3 }}>
                                    <Avatar
                                        sx={{
                                            width: 100,
                                            height: 100,
                                            mx: 'auto',
                                            mb: 2,
                                            bgcolor: 'secondary.main'
                                        }}
                                    >
                                        <AccountCircle sx={{ fontSize: 60 }} />
                                    </Avatar>
                                    <Typography variant="h5" gutterBottom>
                                        {userData?.full_name}
                                    </Typography>
                                    <Typography color="textSecondary" gutterBottom>
                                        {userData?.email}
                                    </Typography>
                                    <Box sx={{
                                        display: 'inline-block',
                                        px: 2,
                                        py: 0.5,
                                        borderRadius: 1,
                                        bgcolor: userData?.is_active ? 'success.light' : 'error.light',
                                        color: userData?.is_active ? 'success.dark' : 'error.dark',
                                        mb: 2
                                    }}>
                                        {userData?.is_active ? "Active" : "Inactive"}
                                    </Box>
                                </Box>
                                <Button
                                    fullWidth
                                    variant="outlined"
                                    onClick={() => navigate('/profile')}
                                    startIcon={<SettingsIcon />}
                                >
                                    Manage Profile
                                </Button>
                            </CardContent>
                        </Card>
                    </Grid>

                    {/* Assistants Grid */}
                    <Grid item xs={12} md={8}>
                        <Typography variant="h5" gutterBottom sx={{ px: 1 }}>
                            Your AI Assistants
                        </Typography>
                        <Grid container spacing={3}>
                            {assistants.map((assistant) => (
                                <Grid item xs={12} key={assistant.id}>
                                    <Paper
                                        elevation={2}
                                        sx={{
                                            p: 3,
                                            transition: 'transform 0.2s, box-shadow 0.2s',
                                            '&:hover': {
                                                transform: 'translateY(-2px)',
                                                boxShadow: 4
                                            }
                                        }}
                                    >
                                        <Grid container spacing={2} alignItems="center">
                                            <Grid item>
                                                <Avatar
                                                    src={assistant.operator_pic}
                                                    sx={{ width: 64, height: 64 }}
                                                />
                                            </Grid>
                                            <Grid item xs>
                                                <Box>
                                                    <Typography variant="h6">
                                                        {assistant.operator_name}
                                                    </Typography>
                                                    <Typography variant="subtitle1" color="textSecondary">
                                                        {assistant.name}
                                                    </Typography>
                                                    <Typography variant="body2" sx={{ mt: 1 }}>
                                                        {assistant.mission}
                                                    </Typography>
                                                    <Box sx={{
                                                        display: 'flex',
                                                        alignItems: 'center',
                                                        mt: 1,
                                                        color: 'text.secondary'
                                                    }}>
                                                        <LinkIcon sx={{ fontSize: 16, mr: 0.5 }} />
                                                        <Typography variant="caption">
                                                            {assistant.url}
                                                        </Typography>
                                                    </Box>
                                                </Box>
                                            </Grid>
                                            <Grid item sx={{ display: 'flex', gap: 1 }}>
                                                <IconButton
                                                    color="error"
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        setSelectedAssistant(assistant);
                                                        setDeleteConfirmOpen(true);
                                                    }}
                                                >
                                                    <DeleteIcon />
                                                </IconButton>
                                                <IconButton
                                                    color="primary"
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        setAssistantToUpdate({ ...assistant });
                                                        setUpdateDialog(true);
                                                    }}
                                                >
                                                    <EditIcon />
                                                </IconButton>
                                                <Button
                                                    variant="contained"
                                                    startIcon={<ChatIcon />}
                                                    color="primary"
                                                    onClick={() => navigate(`/chat/${assistant.id}`)}
                                                >
                                                    Start Chat
                                                </Button>
                                            </Grid>
                                        </Grid>
                                    </Paper>
                                </Grid>
                            ))}
                        </Grid>
                    </Grid>
                </Grid>

                {/* Create Assistant Dialog */}
                <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
                    <DialogTitle>Create New Assistant</DialogTitle>
                    <DialogContent>
                        <TextField
                            fullWidth
                            label="Name"
                            margin="normal"
                            value={newAssistant.name}
                            onChange={(e) => setNewAssistant({ ...newAssistant, name: e.target.value })}
                        />
                        <TextField
                            fullWidth
                            label="URL"
                            margin="normal"
                            value={newAssistant.url}
                            onChange={(e) => setNewAssistant({ ...newAssistant, url: e.target.value })}
                        />
                        <TextField
                            fullWidth
                            label="Mission"
                            margin="normal"
                            value={newAssistant.mission}
                            onChange={(e) => setNewAssistant({ ...newAssistant, mission: e.target.value })}
                        />
                        <TextField
                            fullWidth
                            label="Description"
                            margin="normal"
                            multiline
                            rows={3}
                            value={newAssistant.description}
                            onChange={(e) => setNewAssistant({ ...newAssistant, description: e.target.value })}
                        />
                        <TextField
                            fullWidth
                            label="Operator Name"
                            margin="normal"
                            value={newAssistant.operator_name}
                            onChange={(e) => setNewAssistant({ ...newAssistant, operator_name: e.target.value })}
                        />
                        <TextField
                            fullWidth
                            select
                            label="Authorizations"
                            margin="normal"
                            SelectProps={{ multiple: true }}
                            value={newAssistant.authorizations}
                            onChange={(e) => setNewAssistant({ ...newAssistant, authorizations: e.target.value })}
                        >
                            <MenuItem value="CAN_SEND_EMAIL">Can Send Email</MenuItem>
                            <MenuItem value="CAN_READ_DOCUMENTS">Can Read Documents</MenuItem>
                        </TextField>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
                        <Button onClick={handleCreateAssistant} variant="contained">Create</Button>
                    </DialogActions>
                </Dialog>

                {/* Delete Confirmation Dialog */}
                <Dialog
                    open={deleteConfirmOpen}
                    onClose={() => {
                        setDeleteConfirmOpen(false);
                        setSelectedAssistant(null);
                    }}
                >
                    <DialogTitle>Confirm Delete</DialogTitle>
                    <DialogContent>
                        <Typography>
                            Are you sure you want to delete the assistant "{selectedAssistant?.operator_name}"?
                            This action cannot be undone.
                        </Typography>
                    </DialogContent>
                    <DialogActions>
                        <Button
                            onClick={() => {
                                setDeleteConfirmOpen(false);
                                setSelectedAssistant(null);
                            }}
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={handleDeleteAssistant}
                            color="error"
                            variant="contained"
                        >
                            Delete
                        </Button>
                    </DialogActions>
                </Dialog>

                {/* Update Assistant Dialog */}
                <Dialog
                    open={updateDialog}
                    onClose={() => {
                        setUpdateDialog(false);
                        setAssistantToUpdate(null);
                    }}
                    maxWidth="sm"
                    fullWidth
                >
                    <DialogTitle>Update Assistant</DialogTitle>
                    <DialogContent>
                        <TextField
                            fullWidth
                            label="Name"
                            margin="normal"
                            value={assistantToUpdate?.name || ''}
                            onChange={(e) => setAssistantToUpdate({
                                ...assistantToUpdate,
                                name: e.target.value
                            })}
                        />
                        <TextField
                            fullWidth
                            label="URL"
                            margin="normal"
                            value={assistantToUpdate?.url || ''}
                            onChange={(e) => setAssistantToUpdate({
                                ...assistantToUpdate,
                                url: e.target.value
                            })}
                        />
                        <TextField
                            fullWidth
                            label="Mission"
                            margin="normal"
                            value={assistantToUpdate?.mission || ''}
                            onChange={(e) => setAssistantToUpdate({
                                ...assistantToUpdate,
                                mission: e.target.value
                            })}
                        />
                        <TextField
                            fullWidth
                            label="Description"
                            margin="normal"
                            multiline
                            rows={3}
                            value={assistantToUpdate?.description || ''}
                            onChange={(e) => setAssistantToUpdate({
                                ...assistantToUpdate,
                                description: e.target.value
                            })}
                        />
                        <TextField
                            fullWidth
                            label="Operator Name"
                            margin="normal"
                            value={assistantToUpdate?.operator_name || ''}
                            onChange={(e) => setAssistantToUpdate({
                                ...assistantToUpdate,
                                operator_name: e.target.value
                            })}
                        />
                        <TextField
                            fullWidth
                            select
                            label="Authorizations"
                            margin="normal"
                            SelectProps={{ multiple: true }}
                            value={assistantToUpdate?.authorizations || []}
                            onChange={(e) => setAssistantToUpdate({
                                ...assistantToUpdate,
                                authorizations: e.target.value
                            })}
                        >
                            <MenuItem value="CAN_SEND_EMAIL">Can Send Email</MenuItem>
                            <MenuItem value="CAN_READ_DOCUMENTS">Can Read Documents</MenuItem>
                        </TextField>
                    </DialogContent>
                    <DialogActions>
                        <Button
                            onClick={() => {
                                setUpdateDialog(false);
                                setAssistantToUpdate(null);
                            }}
                        >
                            Cancel
                        </Button>
                        <Button
                            onClick={handleUpdateAssistant}
                            variant="contained"
                            color="primary"
                        >
                            Update
                        </Button>
                    </DialogActions>
                </Dialog>
            </Container>
        </PrivateLayout>
    );
};

export default Dashboard; 