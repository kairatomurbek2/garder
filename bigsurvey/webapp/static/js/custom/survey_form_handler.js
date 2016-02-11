"use strict";

!(function (window) {

    var FormHandler = {
        elements : {
            hazardAssemblyTypeFieldIdSelector: null,
            $surveyDateInput: null,
            serviceType: null,
            custNumber: null,
            surveyHazardsId: null,
            surveyFormPrefix: null,
            surveyFormHazardsName: null,

            bpDeviceFormTriggerOptions: null,
            $hazardSubmitBtnIdSelectorPrefix: null,
            $hazardModal: null,
            hazardFormSpanIdSelectorPrefix: null,
            hazardFormSpanIdSelector: null,
            addHazardBtnClickCount: null,
            currentFormSpanIdSelector: null,
            $hazardFormSpan: null,
            $hazardFormSpanClone: null,
            $hazardModalContentDiv: null,
            includedBPFormIdSelector: null,
            $closeModalBtn: null,
            $addHazardBtn: null,
            $thisFieldIsRequiredErrorMessage: null,
            surveyFormSubmitBtn: null,
            $hazardFormsQtyHolder: null,
            $bpFormsQtyHolder: null
        },
        init: function (options) {
            $.extend(this.elements, options);
            this._initElements();
            this._attachEvents();
            return this;
        },
        _initElements: function () {
            this.elements.bpDeviceFormTriggerOptions = ['installed', 'due_replace', 'maintenance'];
            this.elements.$hazardSubmitBtnIdSelectorPrefix = '#hazard-submit-button-';
            this.elements.$hazardModal = $('#hazard-form-modal');
            this.elements.hazardFormSpanIdSelectorPrefix = '#hazard-and-bp-forms-';
            this.elements.hazardFormSpanIdSelector = this.elements.hazardFormSpanIdSelectorPrefix + '0';
            this.elements.addHazardBtnClickCount = 0;
            this.elements.currentFormSpanIdSelector = this.elements.hazardFormSpanIdSelector.replace('0', String(this.elements.addHazardBtnClickCount));
            this.elements.$hazardFormSpan = $(this.elements.hazardFormSpanIdSelector);
            this.elements.$hazardFormSpanClone = this.elements.$hazardFormSpan.clone(true);
            this.elements.$hazardModalContentDiv = $('#hazard-modal-content');
            this.elements.includedBPFormIdSelector = '#includedBPForm-0';
            this.elements.$closeModalBtn = $('.uk-modal-close');
            this.elements.$addHazardBtn = $('#add_hazard_link');
            this.elements.$thisFieldIsRequiredErrorMessage = $("<p></p>").text("This field is required").addClass('errorlist');
            this.elements.surveyFormSubmitBtn = $('#survey-form-submit-btn');
            this.elements.$hazardFormsQtyHolder = $('#id_hazard-TOTAL_FORMS');
            this.elements.$bpFormsQtyHolder = $('#id_bp-TOTAL_FORMS');
        },

        _attachEvents: function () {
            this.elements.$addHazardBtn.on('click', function () {
                if (!FormHandler.elements.$hazardModal.is(':visible')) {
                    if (FormHandler.elements.addHazardBtnClickCount > 0) {
                        FormHandler.appendFormsCloneAndHideCurrentForm();
                    }
                    FormHandler.updateFormsetsQtyAndIds('up');
                    FormHandler.initGoogleMap.call(FormHandler.elements.$hazardModal);
                    FormHandler.elements.$hazardModal.show();
                    FormHandler.elements.$hazardModal.scrollTop(0);
                    FormHandler.handleHazardAssemblyStatus();
                    FormHandler.elements.addHazardBtnClickCount += 1;
                }
            });

            this.elements.$closeModalBtn.on('click', function () {
                FormHandler.updateFormsetsQtyAndIds('down');
                if (FormHandler.elements.addHazardBtnClickCount > 0) {
                    FormHandler.elements.addHazardBtnClickCount -= 1;
                }
                if ($('.hazard-and-bp-forms').length > 1) {
                    $(FormHandler.elements.currentFormSpanIdSelector).remove()
                } else {
                    FormHandler.resetIncludedForm(FormHandler.elements.currentFormSpanIdSelector);
                }
            });

            this._attachDynamicEvents();

            this.elements.surveyFormSubmitBtn.on('click', function (e) {
                e.preventDefault();
                if (!FormHandler.elements.$surveyDateInput.val()) {
                    FormHandler.elements.$surveyDateInput.parent().append(FormHandler.elements.$thisFieldIsRequiredErrorMessage)
                } else {
                    FormHandler.removeFormSpans();
                    FormHandler.fixRemainingFormSpanAttrs();
                    $('#survey-form').submit();
                }
            });

        },

        _attachDynamicEvents: function () {
            var $currentHazardSubmitBtn = $(FormHandler.elements.$hazardSubmitBtnIdSelectorPrefix + FormHandler.elements.addHazardBtnClickCount);
            $currentHazardSubmitBtn.on('click', function (e) {
                e.preventDefault();
                FormHandler.validateHazardAndBpForm()
            });
        },

        initGoogleMap: function () {
            var newMapHolderId = '#mapholder-' + String(FormHandler.elements.addHazardBtnClickCount);
            var latFieldNameSelector = 'input[name="hazard-0-latitude"]'.replace('0', String(FormHandler.elements.addHazardBtnClickCount));
            var lonFieldNameSelector = 'input[name="hazard-0-longitude"]'.replace('0', String(FormHandler.elements.addHazardBtnClickCount));
            var notificationIdSelector = '#notification-0'.replace('0', String(FormHandler.elements.addHazardBtnClickCount));
            GoogleMap.mapHolder = $(this).find(newMapHolderId);
            GoogleMap.latitudeInput = $(this).find(latFieldNameSelector);
            GoogleMap.longitudeInput = $(this).find(lonFieldNameSelector);
            GoogleMap.notificationLabel = $(this).find(notificationIdSelector);
            GoogleMap.getLocationButton = $('button[data-action="get-location"]');
            GoogleMap.initialize(true);
        },

        handleHazardAssemblyStatus: function () {
            var currentHazardAssemblyTypeFieldIdSelector = FormHandler.elements.hazardAssemblyTypeFieldIdSelector.replace(
                '0', String(FormHandler.elements.addHazardBtnClickCount));
            var currentIncludedBpFormIdSelector = FormHandler.elements.includedBPFormIdSelector.replace(
                '0', String(FormHandler.elements.addHazardBtnClickCount));
            $(currentIncludedBpFormIdSelector).hide();
            var status_select = $(currentHazardAssemblyTypeFieldIdSelector);
            status_select.change(function () {
                FormHandler._triggerBpDeviceForm(currentHazardAssemblyTypeFieldIdSelector, currentIncludedBpFormIdSelector);
            });
        },

        _triggerBpDeviceForm: function (assemblyTypeFieldIdSelector, includedBpFormIdSelector) {
            var statusSelected = $(assemblyTypeFieldIdSelector + " option:selected");
            if (FormHandler._hazardStatusRequiresBpDevice(statusSelected)) {
                $(includedBpFormIdSelector).show();
            }
            else {
                $(includedBpFormIdSelector).hide();
                FormHandler.resetIncludedForm(includedBpFormIdSelector);
            }
        },

        _hazardStatusRequiresBpDevice: function (hazardStatusSelectElem) {
            return $.inArray(hazardStatusSelectElem.val(), FormHandler.elements.bpDeviceFormTriggerOptions) >= 0;
        },

        resetIncludedForm: function (formSelector) {
            $(':input', formSelector)
                .not(':button, :submit, :reset, :hidden')
                .each(function (i, e) {
                    $(e).val($(e).attr('value') || '')
                        .prop('checked', false)
                        .prop('selected', false)
                });
            $('input:text', formSelector).prop('value', '');
            $('option[selected]', formSelector).prop('selected', true);
            $('input[checked]', formSelector).prop('checked', true);
            $('textarea', formSelector).each(function (i, e) {
                $(e).val($(e).html())
            });
            $('.errorlist', formSelector).each(function (i, e) {
                $(e).remove()
            })
        },

        appendFormsCloneAndHideCurrentForm: function () {
            var cloneForNextHazard = FormHandler.elements.$hazardFormSpanClone.clone(true);
            var prevFormSpanIdSelector = FormHandler.elements.hazardFormSpanIdSelectorPrefix + (FormHandler.elements.addHazardBtnClickCount - 1);
            FormHandler.elements.currentFormSpanIdSelector = FormHandler.elements.hazardFormSpanIdSelectorPrefix + FormHandler.elements.addHazardBtnClickCount;

            FormHandler._fixAttrs(cloneForNextHazard, '0', FormHandler.elements.addHazardBtnClickCount);
            cloneForNextHazard.find('*').each(function () {
                var $this = $(this);
                FormHandler._fixAttrs($this, '0', FormHandler.elements.addHazardBtnClickCount);
            });
            $(prevFormSpanIdSelector).addClass('hidden');
            cloneForNextHazard.appendTo(FormHandler.elements.$hazardModalContentDiv);
            FormHandler._attachDynamicEvents();
        },

        _fixAttrs: function (elem, valueToReplace, newValue) {
            var $elem = $(elem);
            if ($elem.attr("id")) {
                $elem.find(["id"]).add(elem).each(function (i, e) {
                    e.id = e.id.replace(valueToReplace, newValue);
                })
            }
            if ($elem.attr("for")) {
                $elem.find(["for"]).add(elem).each(function (i, e) {
                    $(e).attr("for", $(e).attr("for").replace(valueToReplace, newValue));
                })
            }
            if ($elem.attr("name")) {
                $elem.find(["name"]).add(elem).each(function (i, e) {
                    $(e).attr("name", $(e).attr("name").replace(valueToReplace, newValue));
                })
            }
        },

        validateHazardAndBpForm: function () {
            var chosenHazard = $(FormHandler.elements.currentFormSpanIdSelector + ' .hazard-type select option:selected');
            var chosenHazardText = chosenHazard.text() + ', ' + FormHandler.elements.serviceType + ', ' + FormHandler.elements.custNumber;
            var hazardStatus = $(FormHandler.elements.currentFormSpanIdSelector + ' .assembly-status select option:selected');
            var bpDeviceAssemblyTypePresent = $(FormHandler.elements.currentFormSpanIdSelector + ' #assembly-type-present select option:selected');
            if (chosenHazard.val()) {
                if (FormHandler._hazardStatusRequiresBpDevice(hazardStatus) && !bpDeviceAssemblyTypePresent.val()) {
                    FormHandler.elements.$hazardModal.scrollTop(0);
                    $(FormHandler.elements.currentFormSpanIdSelector).find('#assembly-type-present').append(FormHandler.elements.$thisFieldIsRequiredErrorMessage)
                } else {
                    FormHandler._addHazardToCheckList(chosenHazard.val(), chosenHazardText);
                    FormHandler.elements.$hazardModal.hide();
                }
            } else {
                FormHandler.elements.$hazardModal.scrollTop(0);
                $(FormHandler.elements.currentFormSpanIdSelector).find('.hazard-type').append(FormHandler.elements.$thisFieldIsRequiredErrorMessage)
            }
        },

        _addHazardToCheckList: function (value, text) {
            var surveyHazardsId = FormHandler.elements.surveyHazardsId;
            var surveyHazardsIdSelector = '#' + surveyHazardsId;
            var surveyHazardsList = $(surveyHazardsIdSelector);
            var hazardsNumber, nextHazardId, newHazardElement;

            if (surveyHazardsList.length > 0) {
                hazardsNumber = surveyHazardsList[0].childElementCount;
                nextHazardId = surveyHazardsId + '_' + hazardsNumber;
                newHazardElement = FormHandler._createNewHazardElement(nextHazardId, value, text);
                surveyHazardsList.append(newHazardElement);
            } else {
                hazardsNumber = 0;
                var ul = $("<ul></ul>").prop('id', surveyHazardsId);
                nextHazardId = surveyHazardsId + '_' + hazardsNumber;
                newHazardElement = FormHandler._createNewHazardElement(nextHazardId, value, text);
                ul.append(newHazardElement);
                $('#hazards-choices').append(ul);
            }
        },

        _createNewHazardElement: function (elemId, value, text) {
            var li = $("<li></li>");
            var label = $("<label></label>").text(" " + text).prop('for', elemId);
            var inpName = '{{ form.prefix }}' == '' ? 'fake-{{ form.hazards.name }}' : 'fake-{{ form.prefix }}-{{ form.hazards.name }}';
            var inp = $("<input></input>").addClass('uk-width-1-1').attr('data-parent', FormHandler.elements.currentFormSpanIdSelector)
                .prop('id', elemId)
                .prop('name', inpName)
                .prop('type', 'checkbox')
                .prop('value', 'fake-' + value)
                .prop('checked', 'checked');
            label.prepend(inp);
            li.append(label);
            return li
        },

        updateFormsetsQtyAndIds: function (direction) {
            if (direction == 'up') {
                FormHandler._setFormsetsQtyVals(FormHandler.elements.addHazardBtnClickCount + 1)
            }
            if (direction == 'down') {
                if (FormHandler.elements.addHazardBtnClickCount > 0) {
                    FormHandler._setFormsetsQtyVals(FormHandler.elements.addHazardBtnClickCount - 1)
                }
            }
        },

        _setFormsetsQtyVals: function (qty) {
            FormHandler.elements.$hazardFormsQtyHolder.val(qty);
            FormHandler.elements.$bpFormsQtyHolder.val(qty);
        },

        removeFormSpans: function () {
            var uncheckedNewHazardsSpanIds = FormHandler._getNewHazardsSpanIds('unchecked');
            uncheckedNewHazardsSpanIds.forEach(function (spanId) {
                $(spanId).remove()
            });
            var hazardFormsQty = Number(FormHandler.elements.$hazardFormsQtyHolder.val());
            var removedFormSpansQty = uncheckedNewHazardsSpanIds.length;
            FormHandler._setFormsetsQtyVals(hazardFormsQty - removedFormSpansQty)
        },

        _getNewHazardsSpanIds: function (status) {
            var selector;
            if (status == 'unchecked') {
                selector = '#id_survey-hazards input:checkbox:not(:checked)'
            } else {
                selector = '#id_survey-hazards input:checkbox:checked'
            }
            var hazardsSpanIds = [];
            $(selector).each(function () {
                var spanId = $(this).data().parent;
                if (spanId) {
                    hazardsSpanIds.push(spanId)
                }
            });
            return hazardsSpanIds
        },

        fixRemainingFormSpanAttrs: function () {
            var checkedHazardsSpanIds = FormHandler._getNewHazardsSpanIds('checked');
            checkedHazardsSpanIds.forEach(FormHandler._fixFormSpanAttrs);
        },

        _fixFormSpanAttrs: function (element, index, array) {
            var numberToReplace = element.match(/\d/g).join("");
            $(element).find('*').each(function (i, e) {
                FormHandler._fixAttrs(e, numberToReplace, index);
            });
            FormHandler._fixAttrs($(element), numberToReplace, index);
        }

    };
    window.FormHandler = FormHandler;
})(window);