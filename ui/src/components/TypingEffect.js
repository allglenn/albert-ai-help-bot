import React, { useState, useEffect } from 'react';
import { Typography } from '@mui/material';

const TypingEffect = ({ text, speed = 30 }) => {
    const [displayedText, setDisplayedText] = useState('');
    const [currentIndex, setCurrentIndex] = useState(0);

    useEffect(() => {
        if (currentIndex < text.length) {
            const timer = setTimeout(() => {
                setDisplayedText(prev => prev + text[currentIndex]);
                setCurrentIndex(prev => prev + 1);
            }, speed);

            return () => clearTimeout(timer);
        }
    }, [currentIndex, text, speed]);

    // Reset effect when text changes
    useEffect(() => {
        setDisplayedText('');
        setCurrentIndex(0);
    }, [text]);

    return (
        <Typography variant="body1">
            {displayedText}
        </Typography>
    );
};

export default TypingEffect;