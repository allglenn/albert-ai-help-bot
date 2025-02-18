import React, { useState, useEffect } from 'react';
import {
    Container, Typography, Paper, Box, Button, Avatar,
    CircularProgress, Grid, IconButton, Link, List,
    ListItem, ListItemText, ListItemSecondary, ListItemIcon,
    Dialog, DialogTitle, DialogContent, DialogActions,
    Alert, Snackbar, TextField
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
    Search as SearchIcon,
    Article as ArticleIcon,
    Star as StarIcon,
    Description as DescriptionIcon,
    Send as SendIcon
} from '@mui/icons-material';
import TypingEffect from '../../components/TypingEffect';

// Add debounce hook at the top of the file
const useDebounce = (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value);

    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);

        return () => {
            clearTimeout(handler);
        };
    }, [value, delay]);

    return debouncedValue;
};

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
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [searching, setSearching] = useState(false);
    const debouncedSearchQuery = useDebounce(searchQuery, 500); // 500ms delay
    const [chatOpen, setChatOpen] = useState(false);
    const [chatMessage, setChatMessage] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [sendingMessage, setSendingMessage] = useState(false);
    const [chatId, setChatId] = useState(null);
    const [tones, setTones] = useState({});  // Add tones state

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

    // Remove handleSearch function and use useEffect instead
    useEffect(() => {
        const performSearch = async () => {
            if (!debouncedSearchQuery.trim()) {
                setSearchResults([]);
                return;
            }

            setSearching(true);
            try {
                const response = await fetch(
                    `http://localhost:8000/api/v1/help-assistant/${id}/agent/search`,
                    {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ query: debouncedSearchQuery })
                    }
                );

                if (!response.ok) throw new Error('Search failed');

                const data = await response.json();
                setSearchResults(data.results);

            } catch (err) {
                setSnackbar({
                    open: true,
                    message: 'Search failed: ' + err.message,
                    severity: 'error'
                });
            } finally {
                setSearching(false);
            }
        };

        performSearch();
    }, [debouncedSearchQuery, id, token]);

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

    const handleFileOpen = async (filename) => {
        try {
            // Find file by name
            const file = files.find(f => f.filename === filename);
            if (!file) {
                setSnackbar({
                    open: true,
                    message: 'File not found in assistant files',
                    severity: 'error'
                });
                return;
            }

            // Get file URL with auth token
            const fileUrl = `http://localhost:8000/api/v1/help-assistant/${id}/files/${file.id}/download?token=${encodeURIComponent(token)}`;

            // Open in new tab
            window.open(fileUrl, '_blank');

        } catch (err) {
            setSnackbar({
                open: true,
                message: 'Failed to open file: ' + err.message,
                severity: 'error'
            });
        }
    };

    // Add helper function to format IDs
    const formatId = (id) => {
        if (!id) return '';
        return id.slice(-4);
    };

    // Add helper function to highlight search terms
    const highlightSearchTerm = (text, searchTerm) => {
        if (!searchTerm) return text;

        const parts = text.split(new RegExp(`(${searchTerm})`, 'gi'));
        return (
            <>
                {parts.map((part, i) =>
                    part.toLowerCase() === searchTerm.toLowerCase() ?
                        <strong key={i}>{part}</strong> :
                        part
                )}
            </>
        );
    };

    // Add handler for sending messages
    const handleSendMessage = async () => {
        if (!chatMessage.trim()) return;

        setSendingMessage(true);
        try {
            const response = await fetch(
                `http://localhost:8000/api/v1/help-assistant/${id}/chat/${chatId}/message`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ content: chatMessage })
                }
            );
           // console.log("--------Response:---------", response); // Debug log
            if (!response.ok) throw new Error('Failed to send message');

            const data = await response.json();
            //console.log("--------Data:---------", data); // Debug log
            const newMessage = data?.message?.content;
            setChatHistory(prev => [...prev,
            { type: 'user', content: chatMessage },
                { type: 'assistant', content: newMessage, sources: data.sources }
            ]);
            setChatMessage('');

        } catch (err) {
            setSnackbar({
                open: true,
                message: 'Failed to send message: ' + err.message,
                severity: 'error'
            });
        } finally {
            setSendingMessage(false);
        }
    };

    const handleStartChat = async () => {
        try {
            const response = await fetch(
                `http://localhost:8000/api/v1/help-assistant/${id}/chat/init`,
                {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (!response.ok) {
                const error = await response.json();
                if (error.detail.includes("Please log out and log in again")) {
                    // Clear token and redirect to login
                    localStorage.removeItem('token');
                    navigate('/login');
                    return;
                }
                throw new Error(error.detail);
            }

            const data = await response.json();
            setChatId(data.chat_id);
            setChatHistory(data.messages.map(msg => ({
                type: msg.emitter.toLowerCase(),
                content: msg.content,
                timestamp: new Date(msg.created_at)
            })));
            setChatOpen(true);

        } catch (err) {
            setSnackbar({
                open: true,
                message: 'Failed to start chat: ' + err.message,
                severity: 'error'
            });
        }
    };

    // Add function to get tone description
    const getToneDescription = (tone) => {
        // You can fetch these from your API or store them client-side
        const toneDescriptions = {
            PROFESSIONAL: "Formel et professionnel",
            FRIENDLY: "Chaleureux et accessible",
            CASUAL: "Décontracté et informel",
            EMPATHETIC: "Compréhensif et compatissant",
            TECHNICAL: "Précis et technique",
            EDUCATIONAL: "Pédagogique et instructif",
            HUMOROUS: "Léger et humoristique"
        };
        return toneDescriptions[tone] || tone;
    };

    // Add useEffect to fetch tones
    useEffect(() => {
        const fetchTones = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/v1/help-assistant/tones', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch tones');
                }

                const tonesData = await response.json();
                setTones(tonesData);
            } catch (error) {
                console.error('Failed to fetch tones:', error);
            }
        };
        fetchTones();
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
            <Container maxWidth="xl" sx={{ py: 4 }}>
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

                <Grid container spacing={3}>
                    {/* Left Column - Profile, Collection, and Files */}
                    <Grid item xs={12} md={8}>
                        {/* Profile Card */}
                        <Paper elevation={3} sx={{ p: 4, mb: 3 }}>
                            <Grid container spacing={4}>
                                <Grid item xs={12} md={4} sx={{ textAlign: 'center' }}>
                                    <Avatar
                                        src={assistant.operator_pic}
                                        sx={{ width: 200, height: 200, mx: 'auto', mb: 2 }}
                                    />
                                    <Typography variant="h5" gutterBottom>
                                        {assistant.operator_name}
                                    </Typography>
                                    <Typography variant="subtitle1" color="textSecondary">
                                        {getToneDescription(assistant.tone)}
                                    </Typography>
                                    <Button
                                        variant="contained"
                                        startIcon={<ChatIcon />}
                                        onClick={handleStartChat}
                                        sx={{ width: '100%' }}
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

                        {/* Collection Card */}
                        <Paper elevation={3} sx={{ p: 4, mb: 3 }}>
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
                                            {formatId(collection.albert_id)}
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

                        {/* Files Card */}
                        <Paper elevation={3} sx={{ p: 4 }}>
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
                                                    {(file.assistant_collection_id || file.albert_ai_id) && (
                                                        <>
                                                            <br />
                                                            {file.assistant_collection_id && (
                                                                <>Collection: {formatId(file.assistant_collection_id)}</>
                                                            )}
                                                            {file.assistant_collection_id && file.albert_ai_id && (
                                                                <> • </>
                                                            )}
                                                            {file.albert_ai_id && (
                                                                <>Doc: {formatId(file.albert_ai_id)}</>
                                                            )}
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
                    </Grid>

                    {/* Right Column - Search */}
                    <Grid item xs={12} md={4}>
                        <Paper
                            elevation={3}
                            sx={{
                                p: 4,
                                position: { md: 'sticky' },
                                top: { md: '24px' },
                                maxHeight: { md: 'calc(100vh - 48px)' },
                                overflowY: 'auto'
                            }}
                        >
                            <Typography variant="h6" gutterBottom>
                                Search in knowledge base
                            </Typography>
                            <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
                                <TextField
                                    fullWidth
                                    label="Search Query"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                    InputProps={{
                                        endAdornment: searching && (
                                            <CircularProgress
                                                size={20}
                                                sx={{ mr: 1 }}
                                            />
                                        )
                                    }}
                                />
                            </Box>

                            {searchResults.length > 0 && (
                                <List>
                                    {searchResults.map((result, index) => (
                                        <ListItem
                                            key={index}
                                            sx={{
                                                mb: 2,
                                                backgroundColor: 'background.paper',
                                                borderRadius: 1,
                                                border: '1px solid',
                                                borderColor: 'divider',
                                                '&:hover': {
                                                    backgroundColor: 'action.hover'
                                                }
                                            }}
                                        >
                                            <ListItemText
                                                primary={
                                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                            <ArticleIcon color="primary" sx={{ fontSize: 20 }} />
                                                            <Typography variant="subtitle1" color="primary">
                                                                Result {index + 1}
                                                            </Typography>
                                                        </Box>
                                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                            <StarIcon
                                                                sx={{
                                                                    fontSize: 18,
                                                                    color: result.score > 0.7 ? 'success.main' : 'text.secondary'
                                                                }}
                                                            />
                                                            <Typography
                                                                variant="caption"
                                                                sx={{
                                                                    color: result.score > 0.7 ? 'success.main' : 'text.secondary',
                                                                    fontWeight: 'medium'
                                                                }}
                                                            >
                                                                Score: {result.score.toFixed(2)}
                                                            </Typography>
                                                        </Box>
                                                    </Box>
                                                }
                                                secondary={
                                                    <Box sx={{ pl: 3.5 }}>
                                                        <Typography
                                                            component="div"
                                                            variant="body2"
                                                            sx={{
                                                                mb: 1,
                                                                color: 'text.primary',
                                                                lineHeight: 1.6
                                                            }}
                                                        >
                                                            {highlightSearchTerm(result.content, searchQuery)}
                                                        </Typography>
                                                        {result.metadata && Object.keys(result.metadata).length > 0 && (
                                                            <Box sx={{
                                                                mt: 1,
                                                                pt: 1,
                                                                borderTop: '1px solid',
                                                                borderColor: 'divider',
                                                                display: 'flex',
                                                                alignItems: 'center',
                                                                gap: 1
                                                            }}>
                                                                <DescriptionIcon
                                                                    sx={{
                                                                        fontSize: 16,
                                                                        color: 'text.secondary'
                                                                    }}
                                                                />
                                                                <Link
                                                                    component="button"
                                                                    variant="caption"
                                                                    onClick={() => handleFileOpen(result.metadata.document_name)}
                                                                    sx={{
                                                                        fontWeight: 'medium',
                                                                        cursor: 'pointer',
                                                                        '&:hover': {
                                                                            textDecoration: 'underline'
                                                                        }
                                                                    }}
                                                                >
                                                                    From: {result.metadata.document_name}
                                                                </Link>
                                                            </Box>
                                                        )}
                                                    </Box>
                                                }
                                            />
                                        </ListItem>
                                    ))}
                                </List>
                            )}
                        </Paper>
                    </Grid>
                </Grid>

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

                <Dialog
                    open={chatOpen}
                    onClose={() => setChatOpen(false)}
                    maxWidth="md"
                    fullWidth
                    sx={{
                        '& .MuiDialog-paper': {
                            height: '80vh',
                            display: 'flex',
                            flexDirection: 'column'
                        }
                    }}
                >
                    <DialogTitle sx={{ pb: 2, borderBottom: '1px solid', borderColor: 'divider' }}>
                        <Box sx={{ display: 'flex', gap: 2 }}>
                            <Avatar
                                src={assistant.operator_pic}
                                sx={{ width: 48, height: 48 }}
                            />
                            <Box>
                                <Typography variant="h6" sx={{ mb: 0.5 }}>
                                    {assistant.operator_name}
                                </Typography>
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <Typography variant="subtitle2" color="primary">
                                        {assistant.name}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary" sx={{ mx: 1 }}>
                                        •
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        {assistant.mission}
                                    </Typography>
                                </Box>
                            </Box>
                        </Box>
                    </DialogTitle>

                    <DialogContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                        <Box sx={{
                            flexGrow: 1,
                            overflowY: 'auto',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: 2,
                            mb: 2
                        }}>
                            {chatHistory.map((message, index) => (
                                <Box
                                    key={index}
                                    sx={{
                                        alignSelf: message.type === 'user' ? 'flex-end' : 'flex-start',
                                        maxWidth: '80%'
                                    }}
                                >
                                    <Paper
                                        elevation={1}
                                        sx={{
                                            p: 2,
                                            backgroundColor: message.type === 'user' ? 'primary.main' : 'background.paper',
                                            color: message.type === 'user' ? 'primary.contrastText' : 'text.primary'
                                        }}
                                    >
                                        {message.type === 'assistant' ? (
                                            <TypingEffect text={message.content} />
                                        ) : (
                                            <Typography variant="body1">
                                                {message.content}
                                            </Typography>
                                        )}

                                        {message.sources && (
                                            <Box sx={{ mt: 1, pt: 1, borderTop: '1px solid', borderColor: 'divider' }}>
                                                <Typography variant="caption" color="text.secondary">
                                                    Sources: {message.sources.join(', ')}
                                                </Typography>
                                            </Box>
                                        )}
                                    </Paper>
                                </Box>
                            ))}
                        </Box>

                        <Box sx={{ display: 'flex', gap: 1 }}>
                            <TextField
                                fullWidth
                                placeholder="Type your message..."
                                value={chatMessage}
                                onChange={(e) => setChatMessage(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
                                multiline
                                maxRows={4}
                                disabled={sendingMessage}
                            />
                            <IconButton
                                color="primary"
                                onClick={handleSendMessage}
                                disabled={sendingMessage || !chatMessage.trim()}
                                sx={{ alignSelf: 'flex-end' }}
                            >
                                {sendingMessage ? (
                                    <CircularProgress size={24} />
                                ) : (
                                    <SendIcon />
                                )}
                            </IconButton>
                        </Box>
                    </DialogContent>
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