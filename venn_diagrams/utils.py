import pathlib
import pandas as pd

def get_model_predictions(predictions_file_dir: pathlib.Path, lncrna_id_mapping_file_dir: pathlib.Path):
    mart = pd.read_csv(lncrna_id_mapping_file_dir, sep='\t')
    # preprocess model predictions
    preds = pd.read_csv(predictions_file_dir)
    preds = preds.drop(['Unnamed: 0'], axis = 1)
    ids = list(preds['id'])
    preds['ids'] = [e.split('.')[0] for e in ids]
    preds['gold_lab'] = [1 if 'NM' in id else 0 for id in ids]
    # add other ensembl id info
    # the current mapping file contains data only for lncRNAs
    # so we end up removing all coding transcripts in this step
    # also this might be introducing some duplicates
    # (same rna with multiple mappings becomes multiple rows)
    preds = preds.merge(mart, left_on='ids', right_on='Transcript stable ID')

    return preds

def get_ribo_seq_data(ribo_seq_dir: pathlib.Path):
    # specificy some dtypes to prevent warning
    dtypes = {'Chromosome': str, 'Floss-Classification': str, 'Peak shift': str}
    db = pd.read_csv(ribo_seq_dir, sep = '\t', dtype=dtypes)
    db = db[(db['Annotation'] == 'lncrna')]
    return db


def get_cncrnadb_data(cncrnadb_path: pathlib.Path):
    cols = ['cncRNA_id',	'type',	'name',	'gene_id',	'chromosome',
            'start_locus',	'end_locus',	'strand',	'peptide_length',	'tissue',
            'organism',	'genomics',	'peptide_sequence']
    cnc = pd.read_csv(cncrnadb_path, sep='\t', names=cols)
    cnc = cnc.drop([0])
    return cnc


def get_misannotated_lncrnas(preds: pd.DataFrame, mean_cutoff: float, sd_cutoff: float):
    return preds.loc[(preds['mean'] <= mean_cutoff) & (preds['std'] <= sd_cutoff)]


# def get_union_dl_models(cnn_m_lncrnas: pd.DataFrame, 
#                         lstm_m_lncrnas: pd.DataFrame, 
#                         transf_m_lncrnas: pd.DataFrame, 
#                         id_type: str, 
#                         masterIds: set):
#     """Get union of cnn, lstm, tranformer misannotated predictions

#     Args:
#         cnn_m_lncrnas (pd.DataFrame): cnn misannotated predictions
#         lstm_m_lncrnas (pd.DataFrame): lstm misannotated predictions
#         transf_m_lncrnas (pd.DataFrame): transformer misannotated predictions
#         id_type (str): which column to use as id, e.g. 'Gene Stable ID'
#         masterIds (set): the ids that are common across deep learning and other (e.g. ribo or cncrnadb) dataset

#     Returns:
#         set: union of misannotated predictions
#     """
#     cnn_ = set(cnn_m_lncrnas.loc[cnn_m_lncrnas[id_type].isin(masterIds)][id_type])
#     lstm_ = set(lstm_m_lncrnas.loc[lstm_m_lncrnas[id_type].isin(masterIds)][id_type])
#     transf_ = set(transf_m_lncrnas.loc[transf_m_lncrnas[id_type].isin(masterIds)][id_type])

#     dl_i = set.intersection(cnn_, lstm_, transf_)
#     dl_u = set.union(cnn_, lstm_, transf_)
#     print(f'{len(dl_i)} RNAs in DL intersection\n{len(dl_u)} RNAs in DL union')
#     return dl_u