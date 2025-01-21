import React, { useState, useEffect } from 'react';
import {
    Container, Typography, Paper, Box, Button, Avatar,
    CircularProgress, Grid, IconButton, Link, List,
    ListItem, ListItemText, ListItemSecondary, ListItemIcon,
    Dialog, DialogTitle, DialogContent, DialogActions,
    Alert, Snackbar
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import PrivateLayout from '../../components/layout/PrivateLayout';
import {
    Chat as ChatIcon,
    Link as LinkIcon,
    Edit as EditIcon,
    ArrowBack as ArrowBackIcon,
    Upload as UploadIcon,
    Delete as DeleteIcon,
    Description as FileIcon,
    Info as InfoIcon,
} from '@mui/icons-material';

const ShowAssistantPage = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [assistant, setAssistant] = useState(null);
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [uploadOpen, setUploadOpen] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const token = localStorage.getItem('token');
    const [modelsOpen, setModelsOpen] = useState(false);
    const [models, setModels] = useState([]);
    const [loadingModels, setLoadingModels] = useState(false);
    const [collection, setCollection] = useState(null);
    const [loadingCollection, setLoadingCollection] = useState(false);

    const fetchFiles = async () => {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/help-assistant/${id}/files`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            if (!response.ok) throw new Error('Failed to fetch files');
            const data = await response.json();
            setFiles(data);
        } catch (err) {
            setError(err.message);
        }
    };

    const fetchModels = async () => {
        setLoadingModels(true);
        try {
            const response = await fetch('http://localhost:8000/api/v1/help-assistant/models', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });
            if (!response.ok) throw new Error('Failed to fetch models');
            const data = await response.json();
            setModels(data);
        } catch (err) {
            setSnackbar({
                open: true,
                message: 'Failed to load models: ' + err.message,
                severity: 'error'
            });
        } finally {
            setLoadingModels(false);
        }
    };

    const fetchCollection = async () => {
        setLoadingCollection(true);
        try {
            const response = await fetch(
                `http://localhost:8000/api/v1/help-assistant/${id}/collection`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                }
            );
            if (!response.ok) throw new Error('Failed to fetch collection');
            const data = await response.json();
            setCollection(data);
        } catch (err) {
            setSnackbar({
                open: true,
                message: 'Failed to load collection: ' + err.message,
                severity: 'error'
            });
        } finally {
            setLoadingCollection(false);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`http://localhost:8000/api/v1/help-assistant/${id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (!response.ok) throw new Error('Failed to fetch assistant details');
                const data = await response.json();
                setAssistant(data);

                await fetchFiles();
                await fetchCollection();
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id, token]);

    const handleFileUpload = async () => {
        if (!selectedFile) return;

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await fetch(`http://localhost:8000/api/v1/help-assistant/${id}/files`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) throw new Error('Failed to upload file');

            setSnackbar({
                open: true,
                message: 'File uploaded successfully',
                severity: 'success'
            });
            setUploadOpen(false);
            setSelectedFile(null);
            await fetchFiles();
        } catch (err) {
            setSnackbar({
                open: true,
                message: err.message,
                severity: 'error'
            });
        }
    };

    const handleDeleteFile = async (fileId) => {
        try {
            const response = await fetch(`http://localhost:8000/api/v1/help-assistant/${id}/files/${fileId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) throw new Error('Failed to delete file');

            setSnackbar({
                open: true,
                message: 'File deleted successfully',
                severity: 'success'
            });
            await fetchFiles();
        } catch (err) {
            setSnackbar({
                open: true,
                message: err.message,
                severity: 'error'
            });
        }
    };

    // Add helper function to format collection ID
    const formatCollectionId = (id) => {
        if (!id) return '';
        return `${id.slice(-4)}`;
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
                <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
                    <IconButton onClick={() => navigate('/dashboard')}>
                        <ArrowBackIcon />
                    </IconButton>
                    <Typography variant="h4">Assistant Details</Typography>
                    <IconButton
                        color="primary"
                        onClick={() => {
                            setModelsOpen(true);
                            fetchModels();
                        }}
                        sx={{ ml: 'auto' }}
                    >
                        <InfoIcon />
                    </IconButton>
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

                <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
                    <Typography variant="h6" gutterBottom>
                        Collection
                    </Typography>
                    {loadingCollection ? (
                        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                            <CircularProgress />
                        </Box>
                    ) : collection ? (
                        <Box>
                            <Box sx={{ mb: 2 }}>
                                <Typography variant="subtitle1" color="text.secondary">
                                    Collection ID
                                </Typography>
                                <Typography>
                                    {formatCollectionId(collection.albert_id)}
                                </Typography>
                            </Box>
                            <Box sx={{ mb: 2 }}>
                                <Typography variant="subtitle1" color="text.secondary">
                                    Created At
                                </Typography>
                                <Typography>
                                    {new Date(collection.created_at).toLocaleString()}
                                </Typography>
                            </Box>
                        </Box>
                    ) : (
                        <Typography color="text.secondary" align="center">
                            No collection found
                        </Typography>
                    )}
                </Paper>

                <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                        <Typography variant="h6">Files</Typography>
                        <Button
                            variant="contained"
                            startIcon={<UploadIcon />}
                            onClick={() => setUploadOpen(true)}
                        >
                            Upload File
                        </Button>
                    </Box>

                    <List>
                        {files.map((file) => (
                            <ListItem
                                key={file.id}
                                secondaryAction={
                                    <IconButton
                                        edge="end"
                                        aria-label="delete"
                                        onClick={() => handleDeleteFile(file.id)}
                                        color="error"
                                    >
                                        <DeleteIcon />
                                    </IconButton>
                                }
                            >
                                <ListItemIcon>
                                    <FileIcon />
                                </ListItemIcon>
                                <ListItemText
                                    primary={file.filename}
                                    secondary={
                                        <>
                                            Type: {file.file_type} • Size: {(file.file_size / 1024).toFixed(2)} KB
                                            {file.assistant_collection_id && (
                                                <>
                                                    <br />
                                                    Collection: {formatCollectionId(file.assistant_collection_id)}
                                                </>
                                            )}
                                        </>
                                    }
                                />
                            </ListItem>
                        ))}
                        {files.length === 0 && (
                            <Typography color="text.secondary" align="center">
                                No files uploaded yet
                            </Typography>
                        )}
                    </List>
                </Paper>

                <Dialog open={uploadOpen} onClose={() => setUploadOpen(false)}>
                    <DialogTitle>Upload File</DialogTitle>
                    <DialogContent>
                        <input
                            type="file"
                            accept=".pdf,.md,.txt"
                            onChange={(e) => setSelectedFile(e.target.files[0])}
                            style={{ marginTop: '16px' }}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setUploadOpen(false)}>Cancel</Button>
                        <Button
                            onClick={handleFileUpload}
                            variant="contained"
                            disabled={!selectedFile}
                        >
                            Upload
                        </Button>
                    </DialogActions>
                </Dialog>

                <Dialog
                    open={modelsOpen}
                    onClose={() => setModelsOpen(false)}
                    maxWidth="md"
                    fullWidth
                >
                    <DialogTitle>Available AI Models</DialogTitle>
                    <DialogContent>
                        {loadingModels ? (
                            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                                <CircularProgress />
                            </Box>
                        ) : (
                            <List>
                                {models.map((model) => (
                                    <ListItem key={model.id}>
                                        <ListItemText
                                            primary={model.id}
                                            secondary={
                                                <React.Fragment>
                                                    <Typography component="span" variant="body2" color="text.primary">
                                                        Type: {model.type}
                                                    </Typography>
                                                    <br />
                                                    {model.max_context_length && (
                                                        <>
                                                            Max Context Length: {model.max_context_length}
                                                            <br />
                                                        </>
                                                    )}
                                                    Status: {model.status}
                                                    {model.aliases?.length > 0 && (
                                                        <>
                                                            <br />
                                                            Aliases: {model.aliases.join(', ')}
                                                        </>
                                                    )}
                                                </React.Fragment>
                                            }
                                        />
                                    </ListItem>
                                ))}
                            </List>
                        )}
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={() => setModelsOpen(false)}>Close</Button>
                    </DialogActions>
                </Dialog>

                <Snackbar
                    open={snackbar.open}
                    autoHideDuration={6000}
                    onClose={() => setSnackbar({ ...snackbar, open: false })}
                >
                    <Alert
                        onClose={() => setSnackbar({ ...snackbar, open: false })}
                        severity={snackbar.severity}
                        sx={{ width: '100%' }}
                    >
                        {snackbar.message}
                    </Alert>
                </Snackbar>
            </Container>
        </PrivateLayout>
    );
};

export default ShowAssistantPage; 