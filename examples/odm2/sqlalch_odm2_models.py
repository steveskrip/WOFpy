import wof.models as wof_base

class Variable(wof_base.BaseVariable):

    def __init__(self, v=None,
                 VarSampleMedium=None, v_unit=None, v_tunit=None):
        self.VariableCode = v.VariableCode
        self.VariableName = v.VariableNameCV
        self.VariableDescription = v.VariableDefinition
        self.NoDataValue = v.NoDataValue
        self.SampleMedium = VarSampleMedium
        self.DataType = v.VariableTypeCV
        self.Speciation = v.SpeciationCV
        if v_unit is not None:
            self.VariableUnits = Unit(v_unit)
        else:
            self.VariableUnits = None
        if v_tunit is not None:
            self.TimeUnits = Unit(v_tunit)
        else:
            self.TimeUnits = None

    #SampleMedium = wof_base.SampleMediumTypes.NOT_RELEVANT
    #ValueType = Column(String)
    #IsRegular = Column(Boolean)
    #TimeSupport = Column(Float)
    #TimeUnitsID = Column(Integer, ForeignKey('Units.UnitsID'))
    #DataType = Column(String)
    #GeneralCategory = wof_base.GeneralCategoryTypes.WATER_QUALITY

    #VariableUnits = relationship("Units",
    #                    primaryjoin='Variable.VariableUnitsID==Units.UnitsID')

    #TimeUnits = relationship("Units",
    #                    primaryjoin='Variable.TimeUnitsID==Units.UnitsID')

class Site(wof_base.BaseSite):

    def __init__(self, s=None):
        if hasattr(s,'sf_alias') or hasattr(s,'site_alias'):
            self.SiteID = s.sf_alias.SamplingFeatureID
            self.Latitude = s.site_alias.Latitude
            self.Longitude = s.site_alias.Longitude
            self.LatLongDatumID = s.site_alias.SpatialReferenceID
            self.SiteCode = s.sf_alias.SamplingFeatureCode
            self.SiteName = s.sf_alias.SamplingFeatureName
            self.Elevation_m = s.sf_alias.Elevation_m
            self.Comments = s.sf_alias.SamplingFeatureDescription
            sr = wof_base.BaseSpatialReference()
            sr.SpatialReferenceId = s.site_alias.SpatialReferenceObj.SpatialReferenceID
            sr.SRSID = s.site_alias.SpatialReferenceObj.SRSCode
            sr.SRSName = s.site_alias.SpatialReferenceObj.SRSName
            sr.Notes = s.site_alias.SpatialReferenceObj.SRSDescription
            self.LatLongDatum = sr
        else:
            self.SiteID = s.SamplingFeatureID
            self.Latitude = s.Latitude
            self.Longitude = s.Longitude
            self.LatLongDatumID = s.SpatialReferenceID
            self.SiteCode = s.SamplingFeatureObj.SamplingFeatureCode
            self.SiteName = s.SamplingFeatureObj.SamplingFeatureName
            self.Elevation_m = s.SamplingFeatureObj.Elevation_m
            self.Comments = s.SamplingFeatureObj.SamplingFeatureDescription
            sr = wof_base.BaseSpatialReference()
            sr.SpatialReferenceId = s.SpatialReferenceObj.SpatialReferenceID
            sr.SRSID = s.SpatialReferenceObj.SRSCode
            sr.SRSName = s.SpatialReferenceObj.SRSName
            sr.Notes = s.SpatialReferenceObj.SRSDescription
            self.LatLongDatum = sr

class Series(wof_base.BaseSeries):
    def __init__(self, r=None, aff=None):

        fa_obj = r.FeatureActionObj
        u_obj = r.UnitsObj
        v_obj = r.VariableObj
        p_obj = r.ProcessingLevelObj

        sf_obj = fa_obj.SamplingFeatureObj
        a_obj = fa_obj.ActionObj
        m_obj = a_obj.MethodObj
        o_obj = m_obj.OrganizationObj

        self.SeriesID = r.ResultID
        #self.SiteID = fa_obj.SamplingFeatureID
        #self.SiteCode = sf_obj.SamplingFeatureCode
        #self.SiteName = sf_obj.SamplingFeatureName

        self.Variable = Variable(v_obj,
                                 r.SampledMediumCV,
                                 u_obj)
        #self.VariableID = r.VariableID
        #self.VariableCode = v_obj.VariableCode
        #self.VariableName = v_obj.VariableNameCV
        self.SampleMedium = r.SampledMediumCV
        self.QualityControlLevelID = \
            wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][1]
        self.QualityControlLevelCode = \
            wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][0]
        #self.QualityControlLevelCode = p_obj.Definition
        #self.QualityControlLevelID = int(p_obj.ProcessingLevelCode)
        #self.QualityControlLevelID = 0
        #self.MethodID = m_obj.MethodID
        #self.MethodDescription = m_obj.MethodDescription
        self.Method = Method(m_obj)
        self.Organization = o_obj.OrganizationName
        self.BeginDateTimeUTC = a_obj.BeginDateTime
        self.EndDateTimeUTC = a_obj.EndDateTime
        self.ValueCount = r.ValueCount
        self.Source = Source(aff)

class DataValue(wof_base.BaseDataValue):

    def __init__(self,resultType,v,aff_id=None):
        self.ValueID = v.ValueID
        self.DataValue = v.DataValue
        self.DateTimeUTC = v.ValueDateTime
        self.UTCOffset = v.ValueDateTimeUTCOffset
        if aff_id is not None:
            self.SourceID = '%d' % aff_id
        if resultType is 'M':
            self.CensorCode = v.MeasurementResultObj.CensorCodeCV
            self.MethodID = v.MeasurementResultObj.ResultObj.FeatureActionObj.ActionObj.MethodObj.MethodID
        if resultType is 'TS':
            self.CensorCode = v.CensorCodeCV
            self.MethodID = v.TimeSeriesResultObj.ResultObj.FeatureActionObj.ActionObj.MethodObj.MethodID

    QualityControlLevelID = \
        wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][1]
    QualityControlLevel = \
        wof_base.QualityControlLevelTypes['QUAL_CONTROLLED_DATA'][0]


class Method(wof_base.BaseMethod):
    def __init__(self,m_obj):
        self.MethodID = m_obj.MethodID
        self.MethodDescription = m_obj.MethodDescription
        self.MethodLink = m_obj.MethodLink

class Unit(wof_base.BaseUnits):
    def __init__(self,u_obj):
        self.UnitsID = u_obj.UnitsID
        self.UnitsName = u_obj.UnitsName
        self.UnitsType = u_obj.UnitsTypeCV
        self.UnitsAbbreviation = u_obj.UnitsAbbreviation

class Source(wof_base.BaseSource):
    def __init__(self,aff_obj):
        self.SourceID = aff_obj.AffiliationID
        self.Organization = aff_obj.OrganizationObj.OrganizationName
        self.SourceDescription = aff_obj.OrganizationObj.OrganizationDescription
        self.SourceLink = aff_obj.OrganizationObj.OrganizationLink
        self.ContactName = '%s %s' % (aff_obj.PersonObj.PersonFirstName,aff_obj.PersonObj.PersonLastName)
        self.Phone = aff_obj.PrimaryPhone
        self.Email = aff_obj.PrimaryEmail
        self.Address = aff_obj.PrimaryAddress
        #self.City = 'San Diego'
        #self.State = 'CA'
        #self.ZipCode = '92122'
