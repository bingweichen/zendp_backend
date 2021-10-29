#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.image.model import Image
from common import errors
from common.mixins import DictMixin


class Service:
    @staticmethod
    def create(current_user_id, **kwargs):
        new_image = DictMixin.from_dict(Image, kwargs)
        new_image.creator_id = current_user_id
        result = new_image.add()
        if result:
            raise errors.DbCommitFailureException(result)
        return new_image

    # @staticmethod
    # def update_service(image_id, **kwargs):
    #     image = Image.filter_by_company_id(id=image_id).first()
    #     new_image = DictMixin.from_dict(image, kwargs)
    #     result = new_image.update()
    #     if result:
    #         raise errors.DbCommitFailureException(result)
    #     return new_image
    #
    # @staticmethod
    # def delete(image_id):
    #     image = Image.query.filter_by_company_id(id=image_id).first()
    #     result = image.delete()
    #     if result:
    #         raise errors.DbCommitFailureException(result)
    #     return image


