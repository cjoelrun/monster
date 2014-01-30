def feature_archive(features):
    {key: value for (key, value) in
     ((str(x).lower(), x.rpcs_feature) for x in features)}
