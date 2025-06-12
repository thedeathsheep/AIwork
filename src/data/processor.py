"""
Data processor implementation.
"""
from typing import Any, Callable, Dict, List, Optional, Union
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """A flexible data processor for data cleaning and transformation."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.scalers: Dict[str, Any] = {}
        
    def clean_data(self, 
                  data: pd.DataFrame,
                  drop_na: bool = True,
                  fill_na: Optional[Any] = None) -> pd.DataFrame:
        """
        Clean the data by handling missing values.
        
        Args:
            data: Input DataFrame
            drop_na: Whether to drop rows with NA values
            fill_na: Value to fill NA with if drop_na is False
            
        Returns:
            Cleaned DataFrame
        """
        if drop_na:
            data = data.dropna()
        elif fill_na is not None:
            data = data.fillna(fill_na)
            
        return data
    
    def normalize(self, 
                 data: pd.DataFrame,
                 columns: Optional[List[str]] = None,
                 method: str = 'standard') -> pd.DataFrame:
        """
        Normalize numerical columns.
        
        Args:
            data: Input DataFrame
            columns: Columns to normalize (all numerical columns if None)
            method: Normalization method ('standard' or 'minmax')
            
        Returns:
            Normalized DataFrame
        """
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns
            
        for col in columns:
            if col not in self.scalers:
                if method == 'standard':
                    self.scalers[col] = StandardScaler()
                elif method == 'minmax':
                    self.scalers[col] = MinMaxScaler()
                else:
                    raise ValueError(f"Unsupported normalization method: {method}")
                    
                self.scalers[col].fit(data[[col]])
                
            data[col] = self.scalers[col].transform(data[[col]])
            
        return data
    
    def encode_categorical(self, 
                          data: pd.DataFrame,
                          columns: Optional[List[str]] = None,
                          method: str = 'onehot') -> pd.DataFrame:
        """
        Encode categorical columns.
        
        Args:
            data: Input DataFrame
            columns: Columns to encode (all categorical columns if None)
            method: Encoding method ('onehot' or 'label')
            
        Returns:
            Encoded DataFrame
        """
        if columns is None:
            columns = data.select_dtypes(include=['object', 'category']).columns
            
        if method == 'onehot':
            data = pd.get_dummies(data, columns=columns)
        elif method == 'label':
            for col in columns:
                data[col] = data[col].astype('category').cat.codes
        else:
            raise ValueError(f"Unsupported encoding method: {method}")
            
        return data
    
    def apply_transformation(self,
                           data: pd.DataFrame,
                           transform_func: Callable[[pd.DataFrame], pd.DataFrame]) -> pd.DataFrame:
        """
        Apply a custom transformation function to the data.
        
        Args:
            data: Input DataFrame
            transform_func: Function to apply to the data
            
        Returns:
            Transformed DataFrame
        """
