from datetime import datetime
from sqlalchemy import create_engine, distinct, func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import and_

from dateutil.parser import parse

from wof.dao import BaseDao
import sqlalch_odm2_models as model
import api.ODM2.models as odm2_models
from sqlalchemy.orm import aliased
from sqlalchemy import or_
from sqlalchemy import and_

class Odm2Dao(BaseDao):

    def __init__(self, db_connection_string):
        self.engine = create_engine(db_connection_string, convert_unicode=True,
            pool_size=100)
        # Default application pool size is 5. Use 100 to improve performance.
        self.db_session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine))
        odm2_models.Base.query = self.db_session.query_property()

    def __del__(self):
        self.db_session.close()

    def get_all_sites(self):
        s = self.db_session.query(odm2_models.Sites).all()
        s_arr = []
        for i in range(len(s)):
            w_s = model.Site(s[i])
            s_arr.append(w_s)

        site_alias = aliased(odm2_models.Sites, name='site_alias')
        sf_alias = aliased(odm2_models.SamplingFeatures, name='sf_alias')
        rf_alias = aliased(odm2_models.RelatedFeatures, name='rf_alias')
        s = self.db_session.query(site_alias,sf_alias,rf_alias).\
            filter(sf_alias.SamplingFeatureID == rf_alias.SamplingFeatureID,
                   rf_alias.RelatedFeatureID == site_alias.SamplingFeatureID).all()
        #s_arr = []
        for i in range(len(s)):
            w_s = model.Site(s[i])
            s_arr.append(w_s)

        return s_arr

    def get_site_by_code(self, site_code):
        w_s = None
        try:
            s = self.db_session.query(odm2_models.Sites).join(odm2_models.SamplingFeatures).\
                filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code).one()
        except:
            s = None
        if s is None:
            site_alias = aliased(odm2_models.Sites, name='site_alias')
            sf_alias = aliased(odm2_models.SamplingFeatures, name='sf_alias')
            rf_alias = aliased(odm2_models.RelatedFeatures, name='rf_alias')
            try:
                s = self.db_session.query(site_alias,sf_alias,rf_alias).\
                    filter(sf_alias.SamplingFeatureID == rf_alias.SamplingFeatureID,
                           rf_alias.RelatedFeatureID == site_alias.SamplingFeatureID,
                           sf_alias.SamplingFeatureCode == site_code).one()
            except:
                s = None
            if s is not None:
                w_s = model.Site(s)
        else:
            w_s = model.Site(s)
        return w_s

    def get_sites_by_codes(self, site_codes_arr):
        s_arr = []
        for site_code in site_codes_arr:
            w_s = self.get_site_by_code(site_code)
            if w_s is not None:
                s_arr.append(w_s)
        return s_arr

    def get_units_for_variable(self,var_code):
        u = None
        s = None
        try:
            r = self.db_session.query(odm2_models.Results).\
                join(odm2_models.Variables).\
                filter(odm2_models.Variables.VariableCode == var_code).first()
        except:
            r = None
        if r is None:
            try:
                r = self.db_session.query(odm2_models.Results,odm2_models.RelatedFeatures).\
                    join(odm2_models.FeatureActions).\
                    join(odm2_models.SamplingFeatures).\
                    join(odm2_models.Variables.VariableCode).\
                    filter(odm2_models.SamplingFeatures.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                           odm2_models.Variables.VariableCode == var_code).first()
            except:
                r = None
        if r is not None:
            u = r.UnitsObj
            s = r.SampledMediumCV

        return u,s

    def get_units_for_value_for_variable(self,var_code):
        u = None
        s = None
        t = None
        resultType = 'M' #'TS': Time series, 'M':measurement
        try:
            r = self.db_session.query(odm2_models.MeasurementResultValues).\
                    join(odm2_models.MeasurementResults).\
                    join(odm2_models.Results).\
                    join(odm2_models.Variables).\
                    filter(odm2_models.Variables.VariableCode == var_code).first()
        except:
            r = None
        if r is None:
            try:
                r = self.db_session.query(odm2_models.MeasurementResultValues,odm2_models.RelatedFeatures).\
                    join(odm2_models.MeasurementResults).\
                    join(odm2_models.Results).\
                    join(odm2_models.FeatureActions).\
                    join(odm2_models.SamplingFeatures).\
                    join(odm2_models.Variables.VariableCode).\
                    filter(odm2_models.SamplingFeatures.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                           odm2_models.Variables.VariableCode == var_code).first()
            except:
                r = None
        if r is None:
            resultType = 'TS'
            try:
                r = self.db_session.query(odm2_models.TimeSeriesResultValues).\
                        join(odm2_models.TimeSeriesResults).\
                        join(odm2_models.Results).\
                        join(odm2_models.Variables).\
                        filter(odm2_models.Variables.VariableCode == var_code).first()
            except:
                r = None
        if r is None:
            try:
                r = self.db_session.query(odm2_models.TimeSeriesResultValues,odm2_models.RelatedFeatures).\
                    join(odm2_models.TimeSeriesResults).\
                    join(odm2_models.Results).\
                    join(odm2_models.FeatureActions).\
                    join(odm2_models.SamplingFeatures).\
                    join(odm2_models.Variables.VariableCode).\
                    filter(odm2_models.SamplingFeatures.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                           odm2_models.Variables.VariableCode == var_code).first()
            except:
                r = None
        if r is not None:
            if resultType is 'M':
                u = r.MeasurementResultObj.ResultObj.UnitsObj
                s = r.MeasurementResultObj.ResultObj.SampledMediumCV
                t = r.MeasurementResultObj.TimeUnitObj
            if resultType is 'TS':
                u = r.TimeSeriesResultObj.ResultObj.UnitsObj
                s = r.TimeSeriesResultObj.ResultObj.SampledMediumCV
                t = r.TimeUnitObj
        return u,s,t

    def get_all_variables(self):
        v = self.db_session.query(odm2_models.Variables).all()
        v_arr = []
        for i in range(len(v)):
            u,s,t = self.get_units_for_value_for_variable(v[i].VariableCode)
            w_v = model.Variable(v[i],s,u,t)
            v_arr.append(w_v)
        return v_arr

    def get_variable_by_code(self, var_code):
        v = self.db_session.query(odm2_models.Variables).\
            filter(odm2_models.Variables.VariableCode == var_code).first()
        u,s,t = self.get_units_for_value_for_variable(var_code)
        w_v = model.Variable(v,s,u,t)
        return w_v

    def get_variables_by_codes(self, var_codes_arr):
        v = self.db_session.query(odm2_models.Variables).\
            filter(odm2_models.Variables.VariableCode.in_(var_codes_arr)).all()
        v_arr = []
        for i in range(len(v)):
            u,s,t = self.get_units_for_value_for_variable(v[i].VariableCode)
            w_v = model.Variable(v[i],s,u,t)
            v_arr.append(w_v)
        return v_arr

    def get_series_by_sitecode(self, site_code):
        r = self.db_session.query(odm2_models.Results).\
            join(odm2_models.FeatureActions).\
            join(odm2_models.SamplingFeatures).\
            filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code).all()
        if len(r) is 0:
            r = self.db_session.query(odm2_models.Results,odm2_models.RelatedFeatures).\
                join(odm2_models.FeatureActions).\
                join(odm2_models.SamplingFeatures).\
                filter(odm2_models.SamplingFeatures.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                       odm2_models.SamplingFeatures.SamplingFeatureCode == site_code).all()
        r_arr = []
        aff = None
        for i in range(len(r)):
            if i is 0:
                aff = self.db_session.query(odm2_models.Affiliations).\
                    filter(odm2_models.Affiliations.OrganizationID == r[i].FeatureActionObj.ActionObj.MethodObj.OrganizationID).first()
            w_r = model.Series(r[i],aff)
            r_arr.append(w_r)
        return r_arr

    def get_series_by_sitecode_and_varcode(self, site_code, var_code):
        r = self.db_session.query(odm2_models.Results).\
            join(odm2_models.FeatureActions).\
            join(odm2_models.SamplingFeatures).\
            join(odm2_models.Variables).\
            filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code,
                   odm2_models.Variables.VariableCode == var_code).all()
        if len(r) is 0:
            r = self.db_session.query(odm2_models.Results,odm2_models.RelatedFeatures).\
                join(odm2_models.FeatureActions).\
                join(odm2_models.SamplingFeatures).\
                join(odm2_models.Variables.VariableCode).\
                filter(odm2_models.SamplingFeatures.SamplingFeatureID == odm2_models.RelatedFeatures.SamplingFeatureID,
                       odm2_models.SamplingFeatures.SamplingFeatureCode == site_code,
                       odm2_models.Variables.VariableCode == var_code).all()

        r_arr = []
        aff = None
        for i in range(len(r)):
            if i is 0:
                aff = self.db_session.query(odm2_models.Affiliations).\
                  filter(odm2_models.Affiliations.OrganizationID == r[i].FeatureActionObj.ActionObj.MethodObj.OrganizationID).first()
            w_r = model.Series(r[i],aff)
            r_arr.append(w_r)
        return r_arr


    def get_datavalues(self, site_code, var_code, begin_date_time=None,
                       end_date_time=None):
        #siteResult = self.get_site_by_code(site_code)
        #varResult = self.get_variable_by_code(var_code)
        #seriesResult = self.get_series_by_sitecode_and_varcode(site_code,var_code)
        valueResultArr = None
        resultType = 'M' #'TS': Time series, 'M':measurement
        #if siteResult and varResult and seriesResult:
        if (not begin_date_time or not end_date_time):
            try:
                valueResultArr = self.db_session.query(odm2_models.MeasurementResultValues).\
                    join(odm2_models.MeasurementResults).\
                    join(odm2_models.Results).\
                    join(odm2_models.FeatureActions).\
                    join(odm2_models.SamplingFeatures).\
                    join(odm2_models.Variables).\
                    filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code,
                           odm2_models.Variables.VariableCode == var_code).all()
            except:
                valueResultArr = None
            if valueResultArr is None or len(valueResultArr) is 0:
                resultType = 'TS'
                try:
                    valueResultArr = self.db_session.query(odm2_models.TimeSeriesResultValues).\
                        join(odm2_models.TimeSeriesResults).\
                        join(odm2_models.Results).\
                        join(odm2_models.FeatureActions).\
                        join(odm2_models.SamplingFeatures).\
                        join(odm2_models.Variables).\
                        filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code,
                               odm2_models.Variables.VariableCode == var_code).all()
                except:
                    valueResultArr = None
        else:
            begin_date_time = parse(begin_date_time)
            end_date_time = parse(end_date_time)
            try:
                valueResultArr = self.db_session.query(odm2_models.MeasurementResultValues).\
                    join(odm2_models.MeasurementResults).\
                    join(odm2_models.Results).\
                    join(odm2_models.FeatureActions).\
                    join(odm2_models.SamplingFeatures).\
                    join(odm2_models.Variables).\
                    filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code,
                           odm2_models.Variables.VariableCode == var_code,
                           odm2_models.MeasurementResultValues.ValueDateTime >= begin_date_time,
                           odm2_models.MeasurementResultValues.ValueDateTime <= end_date_time).all()
            except:
                valueResultArr = None
            if valueResultArr is None or len(valueResultArr) is 0:
                resultType = 'TS'
                try:
                    valueResultArr = self.db_session.query(odm2_models.TimeSeriesResultValues).\
                        join(odm2_models.TimeSeriesResults).\
                        join(odm2_models.Results).\
                        join(odm2_models.FeatureActions).\
                        join(odm2_models.SamplingFeatures).\
                        join(odm2_models.Variables).\
                        filter(odm2_models.SamplingFeatures.SamplingFeatureCode == site_code,
                               odm2_models.Variables.VariableCode == var_code,
                               odm2_models.TimeSeriesResultValues.ValueDateTime >= begin_date_time,
                               odm2_models.TimeSeriesResultValues.ValueDateTime <= end_date_time).all()
                except:
                    valueResultArr = None
        v_arr = []
        if valueResultArr is not None or len(valueResultArr) is not 0:
            org_id = None
            aff_id = None
            for i in range(len(valueResultArr)):
                if i is 0:
                    if resultType is 'M':
                        org_id = valueResultArr[i].MeasurementResultObj.ResultObj.FeatureActionObj.ActionObj.MethodObj.OrganizationID
                    if resultType is 'TS':
                        org_id = valueResultArr[i].TimeSeriesResultObj.ResultObj.FeatureActionObj.ActionObj.MethodObj.OrganizationID
                    aff_id = self.db_session.query(odm2_models.Affiliations.AffiliationID).\
                            filter(odm2_models.Affiliations.OrganizationID == org_id).first()
                w_v = model.DataValue(resultType,valueResultArr[i],aff_id)
                v_arr.append(w_v)
        return v_arr

    def get_method_by_id(self, method_id):
        m = self.db_session.query(odm2_models.Methods).\
            filter(odm2_models.Methods.MethodID == method_id).one()
        w_m = model.Method(m)
        return w_m

    def get_methods_by_ids(self, method_id_arr):
        m = self.db_session.query(odm2_models.Methods).\
            filter(odm2_models.Methods.MethodID.in_(method_id_arr)).all()
        m_arr = []
        for i in range(len(m)):
            w_m = model.Method(m[i])
            m_arr.append(w_m)
        return m_arr

    def get_source_by_id(self, source_id):
        aff = self.db_session.query(odm2_models.Affiliations).\
            filter(odm2_models.Affiliations.AffiliationID == source_id).one()
        w_aff = model.Source(aff)
        return w_aff

    def get_sources_by_ids(self, source_id_arr):
        aff = self.db_session.query(odm2_models.Affiliations).\
            filter(odm2_models.Affiliations.AffiliationID.in_(source_id_arr)).all()
        aff_arr = []
        for i in range(len(aff)):
            w_a = model.Source(aff[i])
            aff_arr.append(w_a)
        return aff_arr

